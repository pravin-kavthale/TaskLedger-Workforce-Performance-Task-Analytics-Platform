from django.db.models import Q, TextField
from django.db.models.functions import Cast
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from accounts.models import User
from organization.models import Team
from work.models import Assignment, Project, Task

from .models import ActivityLog
from .services import ActivityActionType, ActivityTargetType
from .serializers import ActivityLogSerializer


class ActivityLogPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActivityLogSerializer
    pagination_class = ActivityLogPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "user": ["exact"],
        "action_type": ["exact"],
        "target_type": ["exact"],
        "target_id": ["exact"],
        "created_at": ["gte", "lte"],
    }
    search_fields = ["action_type", "metadata_text", "user__username", "user__email"]
    ordering_fields = ["created_at", "action_type"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        queryset = (
            ActivityLog.objects.select_related("user")
            .annotate(metadata_text=Cast("metadata", TextField()))
            .order_by("-created_at")
        )

        if not user.is_authenticated:
            return queryset.none()

        if user.role == User.Role.ADMIN:
            return queryset

        if user.role == User.Role.MANAGER:
            return queryset.filter(self._manager_visibility_q(user))

        if user.role == User.Role.EMPLOYEE:
            return queryset.filter(self._employee_visibility_q(user))

        return queryset.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        logs = page if page is not None else list(queryset)
        serializer = self.get_serializer(logs, many=True, context=self._serializer_context_for(logs))

        if page is not None:
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context=self._serializer_context_for([instance]))
        return Response(serializer.data)

    def _serializer_context_for(self, logs):
        context = self.get_serializer_context()
        context["target_display_cache"] = self._build_target_display_cache(logs)
        return context

    def _build_target_display_cache(self, logs):
        task_ids = set()
        project_ids = set()
        team_ids = set()

        for log in logs:
            if log.target_type == ActivityTargetType.TASK:
                task_ids.add(log.target_id)
            elif log.target_type == ActivityTargetType.PROJECT:
                project_ids.add(log.target_id)
            elif log.target_type == ActivityTargetType.TEAM:
                team_ids.add(log.target_id)

        cache = {}
        if task_ids:
            cache[ActivityTargetType.TASK] = dict(
                Task.objects.filter(id__in=task_ids).values_list("id", "title")
            )
        if project_ids:
            cache[ActivityTargetType.PROJECT] = dict(
                Project.objects.filter(id__in=project_ids).values_list("id", "name")
            )
        if team_ids:
            cache[ActivityTargetType.TEAM] = dict(
                Team.objects.filter(id__in=team_ids).values_list("id", "name")
            )
        return cache

    def _manager_visibility_q(self, user):
        project_ids = Project.objects.filter(Q(manager=user) | Q(team__manager=user)).values("id")
        team_ids = Team.objects.filter(manager=user).values("id")
        task_ids = Task.objects.filter(
            Q(project__manager=user) | Q(project__team__manager=user)
        ).values("id")

        return (
            Q(user=user)
            | Q(target_type=ActivityTargetType.PROJECT, target_id__in=project_ids)
            | Q(target_type=ActivityTargetType.TEAM, target_id__in=team_ids)
            | Q(target_type=ActivityTargetType.TASK, target_id__in=task_ids)
        )

    def _employee_visibility_q(self, user):
        task_ids = Task.objects.filter(assigned_to=user).values("id")

        project_assignment_q = Q(action_type__in=[
            ActivityActionType.USER_ASSIGNED_TO_PROJECT,
            ActivityActionType.USER_REMOVED_FROM_PROJECT,
            ActivityActionType.USER_ROLE_CHANGED_IN_PROJECT,
        ]) & (
            Q(metadata__user_id__new=user.id)
            | Q(metadata__user_id__old=user.id)
        )

        team_membership_q = Q(action_type__in=[
            ActivityActionType.USER_ADDED_TO_TEAM,
            ActivityActionType.USER_REMOVED_FROM_TEAM,
        ]) & (
            Q(metadata__user_id__new=user.id)
            | Q(metadata__user_id__old=user.id)
        )

        return (
            Q(user=user)
            | Q(target_type=ActivityTargetType.TASK, target_id__in=task_ids)
            | project_assignment_q
            | team_membership_q
        )

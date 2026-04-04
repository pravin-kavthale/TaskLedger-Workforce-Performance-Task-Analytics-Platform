from django.db.models import TextField
from django.db.models.functions import Cast
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from organization.models import Team
from work.models import Project, Task
from core.permissions.services import PermissionService
from core.permissions.scoped_viewsets import BaseScopedReadOnlyViewSet

from .models import ActivityLog
from .services import ActivityTargetType
from .serializers import ActivityLogSerializer

# CRITICAL: NEVER bypass PermissionService for access control.


class ActivityLogPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class ActivityLogViewSet(BaseScopedReadOnlyViewSet):
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
        if not user.is_authenticated:
            return ActivityLog.objects.none()

        base_queryset = (
            ActivityLog.objects.select_related("user")
            .annotate(metadata_text=Cast("metadata", TextField()))
            .order_by("-created_at")
        )

        return PermissionService.scope_activity_logs(user, base_queryset)

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


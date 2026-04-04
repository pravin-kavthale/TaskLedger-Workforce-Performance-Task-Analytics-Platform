from rest_framework import viewsets, mixins

from .helper import is_admin, is_manager, is_project_employee, is_project_manager_of_project, is_team_member
from . models import Assignment, Project, Task
from . serializers import AssignmentSerializer, ProjectMemberSerializer, ProjectSerializer, TaskCreateSerializer, TaskReadSerializer, TaskUpdateSerializer, UserProjectSerializer

from core.permissions import ProjectPermission, AssignmentPermission, TaskPermission, UserProjectPermission

from rest_framework.exceptions import MethodNotAllowed
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from audit.services import (
    ActivityActionType,
    ActivityTargetType,
    log_activity,
)


def _normalize_value(field_name, value):
    if field_name in {"assigned_to", "user", "project", "team", "department", "manager"}:
        return value.id if value is not None else None
    return value


def _extract_changes(instance_before, validated_data, fields):
    changes = {}
    for field in fields:
        if field not in validated_data:
            continue
        old_value = _normalize_value(field, getattr(instance_before, field, None))
        new_value = _normalize_value(field, validated_data.get(field))
        if old_value != new_value:
            changes[field] = {"old": old_value, "new": new_value}
    return changes


def _create_metadata(values):
    return {field: {"old": None, "new": value} for field, value in values.items()}


def _delete_metadata(values):
    return {field: {"old": value, "new": None} for field, value in values.items()}


class ProjectViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [ProjectPermission]
    
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Project.objects.none()
        if is_admin(user):
            return Project.objects.all()
        if is_manager(user):
            return Project.objects.filter(manager=user)
        return Project.objects.filter(assignments__user=user, assignments__is_active=True).distinct()

    def perform_create(self, serializer):
        project = serializer.save(created_by=self.request.user)
        log_activity(
            user=self.request.user,
            action_type=ActivityActionType.PROJECT_CREATED,
            target_type=ActivityTargetType.PROJECT,
            target_id=project.id,
            metadata=_create_metadata({
                "name": project.name,
                "code": project.code,
                "status": project.status,
                "team_id": project.team_id,
                "department_id": project.department_id,
            }),
        )

    def perform_update(self, serializer):
        project = self.get_object()
        tracked_fields = [
            "name",
            "description",
            "department",
            "team",
            "status",
            "start_date",
            "end_date",
        ]
        changes = _extract_changes(project, serializer.validated_data, tracked_fields)
        updated_project = serializer.save()
        if changes:
            log_activity(
                user=self.request.user,
                action_type=ActivityActionType.PROJECT_UPDATED,
                target_type=ActivityTargetType.PROJECT,
                target_id=updated_project.id,
                metadata=changes,
            )

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method, detail="Delete operation is not allowed.")

class AssignmentViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = AssignmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AssignmentPermission]

    def get_queryset(self):
        user = self.request.user
        if is_admin(user):
            return Assignment.objects.select_related("project", "user", "assigned_by")
        if is_manager(user):
            return Assignment.objects.select_related("project", "user", "assigned_by").filter(project__manager_id=user.id)
        return Assignment.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        project = serializer.validated_data["project"]
        assignee = serializer.validated_data["user"]
        if not is_team_member(assignee, project.team):
            raise PermissionDenied("User does not belong to this project's team.")
        assignment = serializer.save(assigned_by=user)
        log_activity(
            user=user,
            action_type=ActivityActionType.USER_ASSIGNED_TO_PROJECT,
            target_type=ActivityTargetType.PROJECT,
            target_id=assignment.project_id,
            metadata=_create_metadata({
                "user_id": assignment.user_id,
                "role": assignment.role,
                "is_active": assignment.is_active,
            }),
        )

    def perform_update(self, serializer):
        assignment = self.get_object()
        project = assignment.project
        assignee = serializer.validated_data.get("user", assignment.user)
        if not is_team_member(assignee, project.team):
            raise PermissionDenied("User does not belong to this project's team.")
        tracked_fields = ["user", "role", "is_active"]
        changes = _extract_changes(assignment, serializer.validated_data, tracked_fields)
        updated_assignment = serializer.save()
        if not changes:
            return

        if "is_active" in changes and changes["is_active"]["new"] is False:
            action_type = ActivityActionType.USER_REMOVED_FROM_PROJECT
        elif "role" in changes:
            action_type = ActivityActionType.USER_ROLE_CHANGED_IN_PROJECT
        elif "user" in changes:
            action_type = ActivityActionType.USER_ASSIGNED_TO_PROJECT
        else:
            action_type = ActivityActionType.USER_ASSIGNED_TO_PROJECT

        log_activity(
            user=self.request.user,
            action_type=action_type,
            target_type=ActivityTargetType.PROJECT,
            target_id=updated_assignment.project_id,
            metadata=changes,
        )

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method, detail="Delete operation is not allowed.")
    
class UserProjectViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserProjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [UserProjectPermission]

    def get_queryset(self):
        user_pk = self.kwargs.get("user_pk")
        if not user_pk:
            return Assignment.objects.none()
        status = self.request.query_params.get("status")
        if status == "current":
            is_active = True
        elif status in ("history", "previous", "completed"):
            is_active = False
        else:
            return Assignment.objects.none()
        return Assignment.objects.filter(user_id=user_pk, is_active=is_active).select_related("project", "assigned_by")
    
class ProjectMemberViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ProjectMemberSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [ProjectPermission]

    def get_queryset(self):
        project_id = self.kwargs.get("project_pk")  
        if project_id is None:
            return Assignment.objects.none()
        status = self.request.query_params.get("status")
        if status == "current":
            is_active = True
        elif status in ("history", "previous", "completed"):
            is_active = False
        else:
            return Assignment.objects.none()
        return Assignment.objects.filter(project_id=project_id, is_active=is_active).select_related("user", "assigned_by")

class ManagerProjectViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_pk = self.kwargs.get("manager_pk")
        requester = self.request.user
        if not user_pk:
            return Project.objects.none()
        try:
            user_pk_int = int(user_pk)
        except ValueError:
            return Project.objects.none()
        if requester.role == User.Role.EMPLOYEE:
            raise PermissionDenied("Employees cannot access this endpoint.")
        if is_manager(requester) and requester.id != user_pk_int:
            raise PermissionDenied("Managers can view only their own projects.")
        return Project.objects.filter(manager_id=user_pk_int)

class TaskViewSet(viewsets.ModelViewSet):
    model = Task
    authentication_classes = [JWTAuthentication]
    permission_classes = [TaskPermission]
    
    def get_queryset(self):
        user = self.request.user
        project_id = self.kwargs.get("project_pk")
        if not project_id:
            return Task.objects.none()
        qs = Task.objects.select_related("project", "assigned_to", "created_by").filter(project_id=project_id)
        if is_admin(user):
            return qs
        is_pm = is_project_manager_of_project(user, project_id)
        is_member = Assignment.objects.filter(project_id=project_id, user=user, is_active=True).exists()
        if is_pm or is_member:
            return qs
        return Task.objects.none()
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TaskReadSerializer
        if self.action == 'create':
            return TaskCreateSerializer
        return TaskUpdateSerializer
    
    def perform_create(self, serializer):
        project_id = self.kwargs.get("project_pk")
        task = serializer.save(project_id=project_id, created_by=self.request.user)
        log_activity(
            user=self.request.user,
            action_type=ActivityActionType.TASK_CREATED,
            target_type=ActivityTargetType.TASK,
            target_id=task.id,
            metadata=_create_metadata({
                "project_id": task.project_id,
                "title": task.title,
                "status": task.status,
                "assigned_to": task.assigned_to_id,
            }),
        )

    def perform_update(self, serializer):
        task = self.get_object()
        tracked_fields = [
            "title",
            "description",
            "priority",
            "estimated_hours",
            "status",
            "assigned_to",
        ]
        changes = _extract_changes(task, serializer.validated_data, tracked_fields)
        updated_task = serializer.save()

        if not changes:
            return

        changed_fields = set(changes.keys())
        detail_fields = {"title", "description", "priority", "estimated_hours"}

        if changed_fields == {"status"}:
            action_type = ActivityActionType.TASK_STATUS_CHANGED
        elif changed_fields == {"assigned_to"}:
            if changes["assigned_to"]["old"] is None:
                action_type = ActivityActionType.TASK_ASSIGNED
            else:
                action_type = ActivityActionType.TASK_REASSIGNED
        elif changed_fields.intersection(detail_fields):
            action_type = ActivityActionType.TASK_DETAILS_UPDATED
        else:
            action_type = ActivityActionType.TASK_STATUS_CHANGED

        log_activity(
            user=self.request.user,
            action_type=action_type,
            target_type=ActivityTargetType.TASK,
            target_id=updated_task.id,
            metadata=changes,
        )

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task_id = task.id
        metadata = {
            "project_id": task.project_id,
            "status": task.status,
            "assigned_to": task.assigned_to_id,
        }
        response = super().destroy(request, *args, **kwargs)
        log_activity(
            user=request.user,
            action_type=ActivityActionType.TASK_DELETED,
            target_type=ActivityTargetType.TASK,
            target_id=task_id,
            metadata=_delete_metadata(metadata),
        )
        return response

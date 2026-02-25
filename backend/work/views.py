from django.shortcuts import render
from rest_framework import viewsets, mixins

from .helper import is_admin, is_project_employee, is_project_manager, is_team_member
from . models import Assignment, Project, Task
from . serializers import AssignmentSerializer, ProjectMemberSerializer, ProjectSerializer, TaskCreateSerializer, TaskReadSerializer, TaskUpdateSerializer, UserProjectSerializer

from core.permissions import ProjectPermission, AssignmentPermission, TaskPermission, UserProjectPermission

from rest_framework.exceptions import MethodNotAllowed
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


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
        if user.role == User.Role.ADMIN:
            return Project.objects.all()
        if user.role == User.Role.MANAGER:
            return Project.objects.filter(manager=user)
        return Project.objects.filter(assignments__user=user, assignments__is_active=True).distinct()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

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
        if user.role == User.Role.MANAGER:
            return Assignment.objects.select_related("project", "user", "assigned_by").filter(project__manager_id=user.id)
        return Assignment.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        project = serializer.validated_data["project"]
        assignee = serializer.validated_data["user"]
        if not is_team_member(assignee, project.team):
            raise PermissionDenied("User does not belong to this project's team.")
        serializer.save(assigned_by=user)

    def perform_update(self, serializer):
        assignment = self.get_object()
        project = assignment.project
        assignee = serializer.validated_data.get("user", assignment.user)
        if not is_team_member(assignee, project.team):
            raise PermissionDenied("User does not belong to this project's team.")
        serializer.save()

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
        if requester.role == User.Role.MANAGER and requester.id != user_pk_int:
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
        is_pm = Project.objects.filter(id=project_id, manager=user).exists()
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
        serializer.save(project_id=project_id, created_by=self.request.user)

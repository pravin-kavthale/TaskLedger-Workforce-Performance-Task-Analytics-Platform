from django.shortcuts import render
from rest_framework import viewsets, mixins
from . models import Assignment, Project
from . serializers import AssignmentSerializer, ProjectMemberSerializer, ProjectSerializer, UserProjectSerializer
from . permissions import CanCreateProject, CanUpdateProject , CanManageProject
from rest_framework.exceptions import MethodNotAllowed
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied



class ProjectViewSet(
    mixins.ListModelMixin,    # GET /projects/                    
    mixins.RetrieveModelMixin,# GET /projects/{id}/                
    mixins.CreateModelMixin,  # POST /projects/
    mixins.UpdateModelMixin,  # PATCH /projects/{id}/
    viewsets.GenericViewSet
):
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]
    

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Project.objects.none()

        if user.role == User.Role.ADMIN:
            return Project.objects.all()

        if user.role == User.Role.MANAGER:
            return Project.objects.filter(manager=user)

        return Project.objects.none()


    def get_permissions(self):
        if self.action == "create":
            return [CanCreateProject()]

        if self.action in ["update", "partial_update"]:
            return [CanUpdateProject()]

        return [IsAuthenticated()]

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == User.Role.ADMIN:
            return Assignment.objects.all()

        if user.role == User.Role.MANAGER:
            return Assignment.objects.filter(project__manager_id=user.id)

        return Assignment.objects.none()

    def perform_create(self, serializer):
        project = serializer.validated_data["project"]
        user = self.request.user

        if not CanManageProject():
            raise PermissionDenied("You cannot assign users to this project.")

        serializer.save(assigned_by=user)

    def perform_update(self, serializer):
        assignment = self.get_object()
        user = self.request.user

        if not CanManageProject():
            raise PermissionDenied("You cannot modify assignments for this project.")

        serializer.save()

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method, detail="Delete operation is not allowed.")

class UserProjectViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserProjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_pk = self.kwargs.get("user_pk")
        requester = self.request.user

        if not user_pk:
            return Assignment.objects.none()

        if requester.role != User.Role.ADMIN and requester.id != int(user_pk):
            raise PermissionDenied("You do not have permission to view this user's projects.")
        
        status = self.request.query_params.get("status")

        if status == "current":
            is_active = True
        elif status in ("history", "previous", "completed"):
            is_active = False
        else:
            # Default fallback if someone sends an invalid status
            return Assignment.objects.none()
        
        return Assignment.objects.filter(
            user_id=user_pk, is_active=is_active
        ).select_related("project", "assigned_by")
    
    
class ProjectMemberViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ProjectMemberSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get("project_pk")  
        user = self.request.user

        if project_id is None:
            return Assignment.objects.none()

        try:
            project = Project.objects.only("id", "manager_id").get(id=project_id)
        except Project.DoesNotExist:
            return Assignment.objects.none()

        if user.role == User.Role.ADMIN:
            pass
        elif user.role == User.Role.MANAGER:
            if project.manager_id != user.id:
                raise PermissionDenied("You are not allowed to view this project.")
        else:
            raise PermissionDenied("You are not allowed to view project members.")

        status = self.request.query_params.get("status")

        if status == "current":
            is_active = True
        elif status in ("history", "previous", "completed"):
            is_active = False
        else:
            # Default fallback if someone sends an invalid status
            return Assignment.objects.none()
            
        

        return (
            Assignment.objects
            .filter(project_id=project_id, is_active=is_active)
            .select_related("user", "assigned_by")
        )
class ManagerProjectViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_pk = self.kwargs.get("user_pk")
        requester = self.request.user

        if not user_pk:
            return Project.objects.none()

        try:
            user_pk = int(user_pk)
        except ValueError:
            return Project.objects.none()

        # Only admins or the manager themselves can access
        if requester.role == User.Role.EMPLOYEE:
            raise PermissionDenied("Employees cannot access this endpoint.")
        if requester.role == User.Role.MANAGER and requester.id != user_pk:
            raise PermissionDenied("Managers can view only their own projects.")

        return Project.objects.filter(manager_id=user_pk)

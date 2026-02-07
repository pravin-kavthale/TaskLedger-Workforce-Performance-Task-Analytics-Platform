from django.shortcuts import render
from rest_framework import viewsets, mixins
from . models import Assignment, Project
from . serializers import AssignmentSerializer, ProjectSerializer
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

        if not CanManageProject(user, assignment.project):
            raise PermissionDenied("You cannot modify assignments for this project.")

        serializer.save()

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method, detail="Delete operation is not allowed.")
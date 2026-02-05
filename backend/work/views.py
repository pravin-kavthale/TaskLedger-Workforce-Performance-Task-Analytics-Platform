from django.shortcuts import render
from rest_framework import viewsets, mixins
from . models import Project
from . serializers import ProjectSerializer
from . permissions import CanCreateProject, CanManageProject, CanUpdateProject
from rest_framework.exceptions import MethodNotAllowed
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.models import User
from rest_framework.permissions import IsAuthenticated


class ProjectViewSet(
    mixins.ListModelMixin,    # GET /projects/
    mixins.RetrieveModelMixin,# GET /projects/{id}/
    mixins.CreateModelMixin,  # POST /projects/
    mixins.UpdateModelMixin, # PATCH /projects/{id}/
    viewsets.GenericViewSet
):
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]
    

    def get_queryset(self):
        user = self.request.user

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
from urllib import request
from django.shortcuts import render
from rest_framework import viewsets, mixins

from accounts.models import User
from work.helper import is_admin
from . models import Department, Team
from . serializers import DepartmentSerializer, TeamSerializer
from . permissions import IsAdminUser, IsAdminOrTeamManager
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status


class DepartmentViewSet(
    mixins.ListModelMixin,    # GET /departments/
    mixins.RetrieveModelMixin,# GET /departments/{id}/
    mixins.CreateModelMixin,  # POST /departments/
    mixins.UpdateModelMixin, # PATCH /departments/{id}/
    viewsets.GenericViewSet
):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def partial_update(self, request, *args, **kwargs):
        # Allow patch only for 'is_active' field
        instance = self.get_object()
        if 'is_active' not in request.data:
            raise MethodNotAllowed(request.method, detail="Only 'is_active' can be updated.")
        return super().partial_update(request, *args, **kwargs)
    
    # Disable PUT and DELETE methods
    
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method, detail="Delete operation is not allowed.")
    
class TeamViewSet(
    mixins.ListModelMixin, # GET /teams/ mixins.RetrieveModelMixin,
    mixins.RetrieveModelMixin, # GET /teams/{id}/ mixins.CreateModelMixin,
    mixins.CreateModelMixin, # POST /teams/ mixins.UpdateModelMixin,
    mixins.UpdateModelMixin, # PATCH /teams/{id}/ viewsets.GenericViewSet
    viewsets.GenericViewSet
):
    serializer_class = TeamSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser, IsAdminOrTeamManager]
    queryset = Team.objects.all()
    
    def get_queryset(self):
        
        user = self.request.user
        if is_admin(user):
            return Team.objects.all()
        
        if user.role == User.Role.MANAGER:
            return Team.objects.filter(manager=user)

        return Team.objects.none()
    
    def perform_create(self, serializer):
        request_user = self.request.user
        if not (is_admin(request_user) or request_user.role == User.Role.MANAGER):
            raise PermissionDenied("You do not have permission to create a team.")
        
        # If manager not set, default to current user if they are manager
        manager = serializer.validated_data.get("manager")
        if not manager:
            if request_user.role == User.Role.MANAGER:
                manager = request_user
            else:
                # Admin must explicitly provide a manager
                raise PermissionDenied("Admin must specify a manager for the team.")

        serializer.save(
            created_by=request_user,
            manager=manager
        )
    
    def perform_update(self, serializer):
        request_user = self.request.user
        team = self.get_object()

        # Only Admin or team manager can update
        if not (is_admin(request_user) or team.manager == request_user):
            raise PermissionDenied("You cannot update this team.")

        # Prevent changing created_by or manager arbitrarily
        validated_data = serializer.validated_data.copy()
        validated_data.pop("created_by", None)
        validated_data.pop("manager", None)  # Optional: Only allow admin to change manager

        serializer.save(**validated_data)
    
    def destroy(self, request, *args, **kwargs):
        request_user = request.user
        team = self.get_object()

        if not (is_admin(request_user) or team.manager == request_user):
            raise PermissionDenied("You cannot delete this team.")

        if not team.is_activate:
            return Response(
                {"detail": "Team already inactive."},
                status=status.HTTP_400_BAD_REQUEST
            )

        team.is_activate = False
        team.save(update_fields=["is_activate"])

        return Response(
            {
                "detail": "Team deactivated successfully."},
            status=status.HTTP_200_OK
        )
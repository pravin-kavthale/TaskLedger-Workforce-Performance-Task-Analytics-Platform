from rest_framework import viewsets, mixins

# CRITICAL: NEVER bypass PermissionService for access control.

from . models import Department, Team
from . serializers import DepartmentSerializer, TeamSerializer, TeamAssignUserSerializer
from core.permissions import TeamPermission, IsAdmin, IsAdminOrTeamManager
from core.permissions.services import PermissionService
from core.permissions.scoped_viewsets import BaseScopedViewSet
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .services.team_service import assign_user_to_team
from audit.services import ActivityActionType, ActivityTargetType, log_activity


class DepartmentViewSet(
    BaseScopedViewSet
):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.none()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return PermissionService.scope_departments(self.request.user, Department.objects.all())

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def partial_update(self, request, *args, **kwargs):
        if 'is_active' not in request.data:
            raise MethodNotAllowed(request.method, detail="Only 'is_active' can be updated.")
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method, detail="Delete operation is not allowed.")
    
class TeamViewSet(
    BaseScopedViewSet
):
    serializer_class = TeamSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [TeamPermission]
    queryset = Team.objects.none()
    
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Team.objects.none()

        return PermissionService.scope_teams(user, Team.objects.all())
    
    def perform_create(self, serializer):
        request_user = self.request.user
        manager = serializer.validated_data.get("manager")
        if not manager:
            if PermissionService.is_manager(request_user):
                manager = request_user
            else:
                raise PermissionDenied("Admin must specify a manager for the team.")

        previous_team_id = manager.team_id if manager else None

        team = serializer.save(
            created_by=request_user,
            manager=manager
        )

        if manager:
            log_activity(
                user=request_user,
                action_type=ActivityActionType.USER_ADDED_TO_TEAM,
                target_type=ActivityTargetType.TEAM,
                target_id=team.id,
                metadata={
                    "user_id": {"old": None, "new": manager.id},
                    "team_id": {"old": previous_team_id, "new": team.id},
                },
            )
    
    def perform_update(self, serializer):
        validated_data = serializer.validated_data.copy()
        validated_data.pop("created_by", None)
        validated_data.pop("manager", None)
        serializer.save(**validated_data)
    
    def destroy(self, request, *args, **kwargs):
        team = self.get_object()
        if not team.is_activate:
            return Response(
                {"detail": "Team already inactive."},
                status=status.HTTP_400_BAD_REQUEST
            )
        team.is_activate = False
        team.save(update_fields=["is_activate"])
        return Response({"detail": "Team deactivated successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrTeamManager], url_path='assign-user')
    def assign_user(self, request, pk=None):
        team = self.get_object()
        serializer = TeamAssignUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        assign_user_to_team(team, user_id, actor=request.user)

        return Response(
            {"message": f"User {user_id} successfully assigned to team."},
            status=status.HTTP_201_CREATED
        )

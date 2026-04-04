from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import User
from .services import PermissionService

class TeamPermission(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if PermissionService.is_admin(request.user):
            return True

        if PermissionService.is_manager(request.user):
            return True

        if request.method == 'POST':
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return PermissionService.can_view_team(request.user, obj)

        return PermissionService.can_manage_team(request.user, obj)

class IsAdminOrTeamManager(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and PermissionService.can_create_team(request.user)

    def has_object_permission(self, request, view, obj):
        return PermissionService.can_manage_team(request.user, obj)

from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import User
from .services import PermissionService

class ProjectPermission(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if PermissionService.is_admin(request.user):
            return True

        project_id = view.kwargs.get('project_pk') or view.kwargs.get('pk')

        if request.method == 'POST' and not project_id:
            team_id = request.data.get('team')
            return bool(team_id) and PermissionService.can_create_project_for_team_id(request.user, team_id)

        if project_id:
            if request.method in SAFE_METHODS:
                return PermissionService.can_view_project_for_id(request.user, project_id)
            return PermissionService.can_update_project_for_id(request.user, project_id)

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return PermissionService.can_view_project(request.user, obj)
        if request.method == 'DELETE':
            return PermissionService.can_delete_project(request.user, obj)
        return PermissionService.can_update_project(request.user, obj)

class UserProjectPermission(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if PermissionService.is_admin(request.user):
            return True

        user_pk = view.kwargs.get('user_pk')
        return bool(user_pk) and PermissionService.can_view_user_projects(request.user, user_pk)

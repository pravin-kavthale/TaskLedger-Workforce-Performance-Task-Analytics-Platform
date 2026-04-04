from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import User
from .services import PermissionService

class AssignmentPermission(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if PermissionService.is_admin(request.user):
            return True

        if request.method == 'POST':
            project_id = request.data.get('project')
            return bool(project_id) and PermissionService.can_assign_user_for_project_id(request.user, project_id)

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return PermissionService.can_view_assignment(request.user, obj)

        return PermissionService.can_update_assignment(request.user, obj)

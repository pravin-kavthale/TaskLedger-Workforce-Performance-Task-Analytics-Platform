from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import User
from .services import PermissionService


class TaskPermission(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if PermissionService.is_admin(request.user):
            return True

        project_id = view.kwargs.get('project_pk')
        if not project_id:
            return False

        if request.method == 'POST':
            return PermissionService.can_create_task_for_project_id(request.user, project_id)

        return PermissionService.can_view_task_collection(request.user, project_id)

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH']:
            return PermissionService.can_update_task(request.user, obj)

        if request.method == 'DELETE':
            return PermissionService.can_delete_task(request.user, obj)

        if request.method in SAFE_METHODS:
            return PermissionService.can_view_task(request.user, obj)

        return False

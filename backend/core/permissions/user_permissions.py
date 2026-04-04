from rest_framework.permissions import BasePermission
from accounts.models import User
from .services import PermissionService

class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        return PermissionService.can_manage_users(request.user)

    def has_object_permission(self, request, view, obj):
        return PermissionService.can_manage_user(request.user, obj)

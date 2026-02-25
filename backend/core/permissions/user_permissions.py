from rest_framework.permissions import BasePermission
from accounts.models import User

class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.role == User.Role.ADMIN:
            return True

        if request.user.role == User.Role.MANAGER:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == User.Role.ADMIN:
            return True

        if user.role == User.Role.MANAGER:
            # Managers can only view/modify/delete employees
            return obj.role == User.Role.EMPLOYEE

        return False

from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import User

class TeamPermission(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.role == User.Role.ADMIN:
            return True

        if request.user.role == User.Role.MANAGER:
            return True

        if request.method == 'POST':
            return False

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == User.Role.ADMIN:
            return True

        if obj.manager == user:
            return True

        if request.method in SAFE_METHODS:
            # Check if they are a member of the team
            return obj.members.filter(id=user.id).exists()

        return False

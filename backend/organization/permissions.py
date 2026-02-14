from rest_framework import permissions
from accounts.models import User

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "ADMIN"

class IsAdminOrTeamManager(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.role == "ADMIN":
            return True
        if user.role == User.Role.MANAGER:
            team_id = view.kwargs.get("pk")
            return user.team and str(user.team.id) == team_id
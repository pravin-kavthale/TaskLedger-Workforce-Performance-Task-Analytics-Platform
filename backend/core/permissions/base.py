from rest_framework.permissions import BasePermission
from backend.accounts.models import User

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Role.ADMIN

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Role.MANAGER

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Role.EMPLOYEE
    
class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in [
            User.Role.ADMIN,
            User.Role.MANAGER
        ]
    
class IsSelfOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == "ADMIN"
            or obj == request.user
        )

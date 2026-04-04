from rest_framework.permissions import BasePermission
from accounts.models import User
from .services import PermissionService

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return PermissionService.is_admin(request.user)

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return PermissionService.is_manager(request.user)

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return PermissionService.is_employee(request.user)
    
class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return PermissionService.can_manage_users(request.user)
    
class IsSelfOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return PermissionService.is_admin(request.user) or obj == request.user

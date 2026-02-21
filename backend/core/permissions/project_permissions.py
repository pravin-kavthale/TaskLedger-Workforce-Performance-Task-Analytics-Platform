from rest_framework.permissions import BasePermission

class IsProjectManagerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == "ADMIN"
            or obj.manager == request.user
        )

class IsAssignedToProject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assignments.filter(user=request.user).exists()

class IsProjectManager(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.manager == request.user

class IsProjectMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assignments.filter(user=request.user).exists()

class IsTaskAssigneeOrManager(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == "ADMIN"
            or obj.project.manager == request.user
            or obj.assigned_to == request.user
        )
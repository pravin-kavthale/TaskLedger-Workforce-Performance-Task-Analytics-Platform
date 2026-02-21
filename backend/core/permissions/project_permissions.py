from rest_framework.permissions import BasePermission

class IsProjectManagerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == "ADMIN"
            or obj.manager == request.user
        )

class IsProjectManager(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.manager == request.user

class IsProjectMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        obj.assignments.filter(user=request.user, is_active=True).exists()

class IsTaskAssigneeOrManager(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == "ADMIN":
            return True

        if obj.assigned_to == request.user:
            return True

        return obj.project.assignments.filter(
            user=request.user,
            role="PROJECT_MANAGER",
            is_active=True
        ).exists()
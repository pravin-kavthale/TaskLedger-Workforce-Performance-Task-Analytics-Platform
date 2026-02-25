from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import User

class AssignmentPermission(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.role == User.Role.ADMIN:
            return True

        if request.method == 'POST':
            project_id = request.data.get('project')
            if project_id:
                from work.models import Project
                return Project.objects.filter(id=project_id, manager=request.user).exists()
            return False

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == User.Role.ADMIN:
            return True

        if obj.project.manager == user:
            return True

        if request.method in SAFE_METHODS:
            return obj.user == user

        return False

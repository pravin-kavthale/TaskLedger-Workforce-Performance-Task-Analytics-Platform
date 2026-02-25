from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import User

class ProjectPermission(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.role == User.Role.ADMIN:
            return True

        project_id = view.kwargs.get('project_pk') or view.kwargs.get('pk')

        if request.method == 'POST' and not project_id:
            if request.user.role == User.Role.MANAGER:
                team_id = request.data.get('team')
                if team_id:
                    from organization.models import Team
                    return Team.objects.filter(id=team_id, manager=request.user).exists()
            return False

        if project_id:
            from work.models import Project, Assignment
            is_pm = Project.objects.filter(id=project_id, manager=request.user).exists()
            if is_pm:
                return True
            if request.method in SAFE_METHODS:
                return Assignment.objects.filter(project_id=project_id, user=request.user, is_active=True).exists()
            return False

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == User.Role.ADMIN:
            return True

        if obj.manager == user:
            return True

        if request.method in SAFE_METHODS:
            from work.models import Assignment
            return Assignment.objects.filter(project=obj, user=user, is_active=True).exists()

        return False

class UserProjectPermission(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.role == User.Role.ADMIN:
            return True

        user_pk = view.kwargs.get('user_pk')
        if user_pk and str(request.user.id) == str(user_pk):
            return True

        return False

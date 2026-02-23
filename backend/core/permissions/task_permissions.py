from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import User

class TaskPermission(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.role == User.Role.ADMIN:
            return True

        project_id = view.kwargs.get('project_pk')
        if not project_id:
            return False

        from work.models import Project, Assignment
        is_pm = Project.objects.filter(id=project_id, manager=request.user).exists()

        if request.method == 'POST':
            return is_pm

        is_member = Assignment.objects.filter(
            project_id=project_id,
            user=request.user,
            is_active=True
        ).exists()

        return is_pm or is_member

    def has_object_permission(self, request, view, obj):
        user = request.user
        from work.models import Task

        if request.method == 'DELETE':
            if obj.status == Task.Status.DONE:
                return False
            if user.role == User.Role.ADMIN:
                return True
            if obj.project.manager == user:
                return True
            return False

        if request.method in ['PUT', 'PATCH']:
            if obj.status == Task.Status.DONE:
                return False

            if user.role == User.Role.ADMIN:
                return True

            if obj.project.manager == user:
                return True

            if obj.assigned_to == user:
                # Employees can only update task status.
                if user.role == User.Role.EMPLOYEE:
                    allowed_fields = {'status'}
                    if set(request.data.keys()) - allowed_fields:
                        return False

                    # BLOCKED cannot be exited by employee
                    if obj.status == Task.Status.BLOCKED:
                        new_status = request.data.get('status')
                        if new_status and new_status != Task.Status.BLOCKED:
                            return False

                # Cannot reassign tasks.
                if 'assigned_to' in request.data:
                    new_assignee = request.data.get('assigned_to')
                    if new_assignee and str(new_assignee) != str(user.id):
                        return False

                return True

            return False

        if request.method in SAFE_METHODS:
            if user.role == User.Role.ADMIN:
                return True
            if obj.project.manager == user:
                return True
            return True

        return False

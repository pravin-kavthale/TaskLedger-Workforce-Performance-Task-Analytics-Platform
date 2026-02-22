from multiprocessing import context
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Project,Assignment
from accounts.models import User
from .helper import is_admin, is_project_manager, is_project_employee, is_project_manager_of_project



class CanCreateProject(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Role.ADMIN


class CanUpdateProject(BasePermission):
    def has_object_permission(self, request, view, obj: Project):
        if request.user.role == User.Role.ADMIN:
            return True

        if (
            request.user.role == User.Role.MANAGER
            and obj.manager_id == request.user.id
        ):
            return True

        return False
    

class CanManageProject(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        # obj is expected to be a Project instance

        if request.user.role == User.Role.ADMIN:
            return True

        if (
            request.user.role == User.Role.MANAGER
            and obj.manager_id == request.user.id
        ):
            return True

        return False

class TaskBasePermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if is_admin(user):
            return True

        if request.method in SAFE_METHODS:
            return True

        if request.method == 'POST':
            project_id = view.kwargs.get("project_pk")
            if not project_id:
                return False
            return is_project_manager_of_project(user, project_id)

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        project = obj.project

        if is_admin(user):
            return True

        if request.method in SAFE_METHODS:
            return (
                is_project_manager(user, project)
                or is_project_employee(user, project)
            )

        if is_project_manager(user, project):
            return True

        if (
            request.method in ('PUT', 'PATCH')
            and is_project_employee(user, project)
            and obj.assignee_id == user.id
        ):
            return True

        return False

class TaskPermission(BasePermission):
    def has_permission(self, request, view):
        # Unauthenticated users: No access.
        if not (request.user and request.user.is_authenticated):
            return False

        # ADMIN: Full access.
        if request.user.role == User.Role.ADMIN:
            return True

        project_id = view.kwargs.get('project_pk')
        if not project_id:
            return False

        # Check if user is the Project Manager.
        is_pm = Project.objects.filter(id=project_id, manager=request.user).exists()

        # Block POST at has_permission level for unauthorized roles (only PM and ADMIN allowed).
        if request.method == 'POST':
            return is_pm

        # For other methods, check if they are at least a member of the project.
        is_member = Assignment.objects.filter(
            project_id=project_id,
            user=request.user,
            is_active=True
        ).exists()

        return is_pm or is_member

    def has_object_permission(self, request, view, obj):
        user = request.user

        # ADMIN: Full access.
        if user.role == User.Role.ADMIN:
            return True

        # Project Manager: Full access to tasks within their project.
        if obj.project.manager == user:
            return True

        # Safe methods (retrieve) are allowed for all project members.
        # Membership is already checked in has_permission for list/detail.
        if request.method in SAFE_METHODS:
            return True

        # Assigned Member (task.assignee):
        # Note: In the model it is 'assigned_to'.
        if obj.assigned_to == user:
            # Cannot delete tasks.
            if request.method == 'DELETE':
                return False

            # Can partially update their own tasks (e.g., status).
            # Cannot reassign tasks.
            if request.method in ['PUT', 'PATCH']:
                # Enforce "Cannot reassign tasks" by checking request.data
                if 'assigned_to' in request.data:
                    new_assignee = request.data.get('assigned_to')
                    if new_assignee and str(new_assignee) != str(user.id):
                        return False
                return True

        # Other project members cannot update or delete.
        return False

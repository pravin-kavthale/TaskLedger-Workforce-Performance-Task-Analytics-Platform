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

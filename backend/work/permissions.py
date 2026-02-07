from multiprocessing import context
from rest_framework.permissions import BasePermission
from .models import Project
from accounts.models import User


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
    """
    Admin can manage all projects.
    Manager can manage only projects assigned to them.
    """

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
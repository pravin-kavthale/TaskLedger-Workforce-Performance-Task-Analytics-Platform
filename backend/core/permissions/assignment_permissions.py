from rest_framework.permissions import BasePermission
from accounts.models import User

from rest_framework.permissions import BasePermission


class AssignmentPermission(BasePermission):

    def has_permission(self, request, view):
        # Block completely unauthenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        # Admin can do anything
        if request.user.role == "ADMIN":
            return True

        # Project manager of that project can do anything
        if obj.project.manager == request.user:
            return True

        # SAFE METHODS = GET / HEAD / OPTIONS
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            # Assigned member can only see THEIR OWN assignment
            return obj.user == request.user

        # For PATCH, PUT, DELETE — block regular members
        return False
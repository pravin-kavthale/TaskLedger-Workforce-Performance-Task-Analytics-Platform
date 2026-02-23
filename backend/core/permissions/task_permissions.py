from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import User
from work.models import Project, Assignment, Task


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

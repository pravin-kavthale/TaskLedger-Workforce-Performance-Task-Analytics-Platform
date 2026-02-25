from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import User
<<<<<<< HEAD
from work.models import Project, Assignment, Task


class TaskPermission(BasePermission):
    def has_permission(self, request, view):
        # Unauthenticated users: No access.
        if not (request.user and request.user.is_authenticated):
            return False

        # ADMIN: Full access.
=======

class TaskPermission(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

>>>>>>> 256e651804daae79d52c32d1c337a20751aafaf8
        if request.user.role == User.Role.ADMIN:
            return True

        project_id = view.kwargs.get('project_pk')
        if not project_id:
            return False

<<<<<<< HEAD
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
        
=======
        from work.models import Project, Assignment
        is_pm = Project.objects.filter(id=project_id, manager=request.user).exists()

        if request.method == 'POST':
            return is_pm

        is_member = Assignment.objects.filter(
            project_id=project_id,
            user=request.user,
            is_active=True
        ).exists()

>>>>>>> 256e651804daae79d52c32d1c337a20751aafaf8
        return is_pm or is_member

    def has_object_permission(self, request, view, obj):
        user = request.user
<<<<<<< HEAD
        
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
=======
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
>>>>>>> 256e651804daae79d52c32d1c337a20751aafaf8
                if 'assigned_to' in request.data:
                    new_assignee = request.data.get('assigned_to')
                    if new_assignee and str(new_assignee) != str(user.id):
                        return False
<<<<<<< HEAD
                return True
                
        # Other project members cannot update or delete.
=======

                return True

            return False

        if request.method in SAFE_METHODS:
            if user.role == User.Role.ADMIN:
                return True
            if obj.project.manager == user:
                return True
            return True

>>>>>>> 256e651804daae79d52c32d1c337a20751aafaf8
        return False

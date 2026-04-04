from accounts.models import User
from work.models import Assignment


class PermissionService:

    # ---------------- COMMON ---------------- #

    @staticmethod
    def is_admin(user):
        return user.role == User.Role.ADMIN

    @staticmethod
    def is_manager(user):
        return user.role == User.Role.MANAGER

    @staticmethod
    def is_employee(user):
        return user.role == User.Role.EMPLOYEE

    # ---------------- USER ---------------- #

    @staticmethod
    def can_manage_user(user, target_user):
        if PermissionService.is_admin(user):
            return True
        if PermissionService.is_manager(user):
            return target_user.role == User.Role.EMPLOYEE
        return False

    # ---------------- TEAM ---------------- #

    @staticmethod
    def can_manage_team(user, team):
        if PermissionService.is_admin(user):
            return True
        if PermissionService.is_manager(user):
            return team.manager_id == user.id
        return False

    @staticmethod
    def can_view_team(user, team):
        if PermissionService.is_admin(user):
            return True
        if team.manager_id == user.id:
            return True
        return team.members.filter(id=user.id).exists()

    # ---------------- PROJECT ---------------- #

    @staticmethod
    def can_create_project(user, team):
        if PermissionService.is_admin(user):
            return True
        if PermissionService.is_manager(user):
            return team.manager_id == user.id
        return False

    @staticmethod
    def can_view_project(user, project):
        if PermissionService.is_admin(user):
            return True
        if project.manager_id == user.id:
            return True
        return Assignment.objects.filter(
            project=project, user=user, is_active=True
        ).exists()

    @staticmethod
    def can_update_project(user, project):
        if PermissionService.is_admin(user):
            return True
        return project.manager_id == user.id

    @staticmethod
    def can_delete_project(user, project):
        return PermissionService.can_update_project(user, project)

    # ---------------- ASSIGNMENT ---------------- #

    @staticmethod
    def can_assign_user(user, project):
        if PermissionService.is_admin(user):
            return True
        return project.manager_id == user.id

    @staticmethod
    def can_remove_user(user, assignment):
        if PermissionService.is_admin(user):
            return True
        return assignment.project.manager_id == user.id

    @staticmethod
    def can_view_assignment(user, assignment):
        if PermissionService.is_admin(user):
            return True
        if assignment.project.manager_id == user.id:
            return True
        return assignment.user_id == user.id

    # ---------------- TASK ---------------- #

    @staticmethod
    def can_create_task(user, project):
        if PermissionService.is_admin(user):
            return True
        return project.manager_id == user.id

    @staticmethod
    def can_view_task(user, task):
        if PermissionService.is_admin(user):
            return True
        if task.project.manager_id == user.id:
            return True
        return Assignment.objects.filter(
            project=task.project, user=user, is_active=True
        ).exists()

    @staticmethod
    def can_update_task(user, task):
        if PermissionService.is_admin(user):
            return True
        if task.project.manager_id == user.id:
            return True
        return task.assigned_to_id == user.id

    @staticmethod
    def can_delete_task(user, task):
        if PermissionService.is_admin(user):
            return True
        return task.project.manager_id == user.id

    # ---------------- AUDIT ---------------- #

    @staticmethod
    def can_view_audit_logs(user):
        return user.role in [
            User.Role.ADMIN,
            User.Role.MANAGER,
            User.Role.EMPLOYEE,
        ]
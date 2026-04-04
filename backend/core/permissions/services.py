from django.db.models import Q, TextField
from django.db.models.functions import Cast

from accounts.models import User
from organization.models import Department, Team
from work.models import Assignment, Project, Task


# CRITICAL: NEVER bypass PermissionService for access control.


def _validate_scope_inputs(user, queryset):
    if user is None:
        raise ValueError("User must be provided")
    if queryset is None:
        raise ValueError("Queryset must be provided")
    if getattr(user, "role", None) not in User.Role.values:
        raise ValueError("User role must be valid")


class PermissionService:

    # ---------------- COMMON ---------------- #

    @staticmethod
    def is_admin(user):
        return bool(user) and user.role == User.Role.ADMIN

    @staticmethod
    def is_manager(user):
        return bool(user) and user.role == User.Role.MANAGER

    @staticmethod
    def is_employee(user):
        return bool(user) and user.role == User.Role.EMPLOYEE

    @staticmethod
    def can_assign_role(user, target_role):
        if PermissionService.is_admin(user):
            return True
        if PermissionService.is_manager(user):
            return target_role == User.Role.EMPLOYEE
        return False

    @staticmethod
    def can_manage_users(user):
        return PermissionService.is_admin(user) or PermissionService.is_manager(user)

    @staticmethod
    def scope_visible_users(user, queryset):
        _validate_scope_inputs(user, queryset)
        if PermissionService.is_admin(user):
            return queryset
        if PermissionService.is_manager(user):
            return queryset.filter(role=User.Role.EMPLOYEE)
        return queryset.none()

    @staticmethod
    def scope_departments(user, queryset):
        _validate_scope_inputs(user, queryset)
        if PermissionService.is_admin(user):
            return queryset
        return queryset.none()

    @staticmethod
    def scope_projects(user, queryset):
        _validate_scope_inputs(user, queryset)
        if PermissionService.is_admin(user):
            return queryset
        if PermissionService.is_manager(user):
            return queryset.filter(manager=user)
        if PermissionService.is_employee(user):
            return queryset.filter(assignments__user=user, assignments__is_active=True).distinct()
        return queryset.none()

    @staticmethod
    def scope_tasks(user, queryset):
        _validate_scope_inputs(user, queryset)
        if PermissionService.is_admin(user):
            return queryset
        if PermissionService.is_manager(user):
            return queryset.filter(project__manager=user)
        if PermissionService.is_employee(user):
            return queryset.filter(assigned_to=user)
        return queryset.none()

    @staticmethod
    def scope_assignments(user, queryset):
        _validate_scope_inputs(user, queryset)
        if PermissionService.is_admin(user):
            return queryset
        if PermissionService.is_manager(user):
            return queryset.filter(project__manager=user)
        if PermissionService.is_employee(user):
            return queryset.filter(user=user)
        return queryset.none()

    @staticmethod
    def scope_user_assignments(user, target_user_id, queryset, *, status=None):
        _validate_scope_inputs(user, queryset)
        if status == "current":
            queryset = queryset.filter(is_active=True)
        elif status in ("history", "previous", "completed"):
            queryset = queryset.filter(is_active=False)
        else:
            return queryset.none()

        queryset = queryset.filter(user_id=target_user_id)
        return PermissionService.scope_assignments(user, queryset)

    @staticmethod
    def scope_project_assignments(user, project_id, queryset, *, status=None):
        _validate_scope_inputs(user, queryset)
        if status == "current":
            queryset = queryset.filter(is_active=True)
        elif status in ("history", "previous", "completed"):
            queryset = queryset.filter(is_active=False)
        else:
            return queryset.none()

        queryset = queryset.filter(project_id=project_id)
        return PermissionService.scope_assignments(user, queryset)

    @staticmethod
    def scope_teams(user, queryset):
        _validate_scope_inputs(user, queryset)
        if PermissionService.is_admin(user):
            return queryset
        if PermissionService.is_manager(user):
            return queryset.filter(manager=user)
        if PermissionService.is_employee(user):
            return queryset.filter(members=user).distinct()
        return queryset.none()

    @staticmethod
    def scope_activity_logs(user, queryset):
        _validate_scope_inputs(user, queryset)

        if PermissionService.is_admin(user):
            return queryset

        if PermissionService.is_manager(user):
            project_ids = Project.objects.filter(Q(manager=user) | Q(team__manager=user)).values("id")
            team_ids = Team.objects.filter(manager=user).values("id")
            task_ids = Task.objects.filter(
                Q(project__manager=user) | Q(project__team__manager=user)
            ).values("id")

            return queryset.filter(
                Q(user=user)
                | Q(target_type="PROJECT", target_id__in=project_ids)
                | Q(target_type="TEAM", target_id__in=team_ids)
                | Q(target_type="TASK", target_id__in=task_ids)
            )

        if PermissionService.is_employee(user):
            task_ids = Task.objects.filter(assigned_to=user).values("id")

            project_assignment_q = Q(action_type__in=[
                "USER_ASSIGNED_TO_PROJECT",
                "USER_REMOVED_FROM_PROJECT",
                "USER_ROLE_CHANGED_IN_PROJECT",
            ]) & (
                Q(metadata__user_id__new=user.id)
                | Q(metadata__user_id__old=user.id)
            )

            team_membership_q = Q(action_type__in=[
                "USER_ADDED_TO_TEAM",
                "USER_REMOVED_FROM_TEAM",
            ]) & (
                Q(metadata__user_id__new=user.id)
                | Q(metadata__user_id__old=user.id)
            )

            return queryset.filter(
                Q(user=user)
                | Q(target_type="TASK", target_id__in=task_ids)
                | project_assignment_q
                | team_membership_q
            )

        return queryset.none()

    # ---------------- USER ---------------- #

    @staticmethod
    def can_manage_user(user, target_user):
        _validate_scope_inputs(user, target_user)
        if PermissionService.is_admin(user):
            return True
        if PermissionService.is_manager(user):
            return target_user.role == User.Role.EMPLOYEE
        return False

    @staticmethod
    def can_view_user_projects(user, target_user_id):
        if user is None:
            raise ValueError("User must be provided")
        if PermissionService.is_admin(user):
            return True
        return str(getattr(user, "id", None)) == str(target_user_id)

    @staticmethod
    def can_view_manager_projects(user, manager_id):
        if user is None:
            raise ValueError("User must be provided")
        if PermissionService.is_admin(user):
            return True
        return PermissionService.is_manager(user) and str(getattr(user, "id", None)) == str(manager_id)

    # ---------------- TEAM ---------------- #

    @staticmethod
    def can_create_team(user):
        return PermissionService.is_admin(user) or PermissionService.is_manager(user)

    @staticmethod
    def can_manage_team(user, team):
        _validate_scope_inputs(user, team)
        if PermissionService.is_admin(user):
            return True
        if PermissionService.is_manager(user):
            return team.manager_id == user.id
        return False

    @staticmethod
    def can_create_team_user_assignment(user, team):
        return PermissionService.can_manage_team(user, team)

    @staticmethod
    def can_view_team(user, team):
        _validate_scope_inputs(user, team)
        if PermissionService.is_admin(user):
            return True
        if team.manager_id == user.id:
            return True
        return team.members.filter(id=user.id).exists()

    @staticmethod
    def is_team_member(user, team):
        _validate_scope_inputs(user, team)
        return team.members.filter(id=user.id).exists()

    # ---------------- PROJECT ---------------- #

    @staticmethod
    def can_create_project(user, team):
        _validate_scope_inputs(user, team)
        if PermissionService.is_admin(user):
            return True
        if PermissionService.is_manager(user):
            return team.manager_id == user.id
        return False

    @staticmethod
    def can_create_project_for_team_id(user, team_id):
        if user is None:
            raise ValueError("User must be provided")
        if PermissionService.is_admin(user):
            return True
        if not PermissionService.is_manager(user):
            return False
        return Team.objects.filter(id=team_id, manager_id=user.id).exists()

    @staticmethod
    def can_view_project(user, project):
        _validate_scope_inputs(user, project)
        if PermissionService.is_admin(user):
            return True
        if project.manager_id == user.id:
            return True
        return Assignment.objects.filter(
            project=project, user=user, is_active=True
        ).exists()

    @staticmethod
    def is_project_member(user, project):
        _validate_scope_inputs(user, project)
        return Assignment.objects.filter(project=project, user=user, is_active=True).exists()

    @staticmethod
    def is_project_member_for_id(user, project_id):
        if user is None:
            raise ValueError("User must be provided")
        return Assignment.objects.filter(project_id=project_id, user=user, is_active=True).exists()

    @staticmethod
    def can_view_project_for_id(user, project_id):
        if user is None:
            raise ValueError("User must be provided")
        if PermissionService.is_admin(user):
            return True
        project = Project.objects.filter(id=project_id).only("id", "manager_id", "team_id").first()
        if not project:
            return False
        if project.manager_id == getattr(user, "id", None):
            return True
        return Assignment.objects.filter(
            project_id=project_id, user=user, is_active=True
        ).exists()

    @staticmethod
    def can_update_project(user, project):
        _validate_scope_inputs(user, project)
        if PermissionService.is_admin(user):
            return True
        return project.manager_id == user.id

    @staticmethod
    def can_update_project_for_id(user, project_id):
        if user is None:
            raise ValueError("User must be provided")
        if PermissionService.is_admin(user):
            return True
        return Project.objects.filter(id=project_id, manager_id=user.id).exists()

    @staticmethod
    def can_delete_project(user, project):
        return PermissionService.can_update_project(user, project)

    @staticmethod
    def can_delete_project_for_id(user, project_id):
        return PermissionService.can_update_project_for_id(user, project_id)

    # ---------------- ASSIGNMENT ---------------- #

    @staticmethod
    def can_assign_user(user, project):
        _validate_scope_inputs(user, project)
        if PermissionService.is_admin(user):
            return True
        return project.manager_id == user.id

    @staticmethod
    def can_assign_user_for_project_id(user, project_id):
        if user is None:
            raise ValueError("User must be provided")
        if PermissionService.is_admin(user):
            return True
        return Project.objects.filter(id=project_id, manager_id=user.id).exists()

    @staticmethod
    def can_remove_user(user, assignment):
        _validate_scope_inputs(user, assignment)
        if PermissionService.is_admin(user):
            return True
        return assignment.project.manager_id == user.id

    @staticmethod
    def can_update_assignment(user, assignment):
        _validate_scope_inputs(user, assignment)
        if PermissionService.is_admin(user):
            return True
        return assignment.project.manager_id == user.id

    @staticmethod
    def can_view_assignment(user, assignment):
        _validate_scope_inputs(user, assignment)
        if PermissionService.is_admin(user):
            return True
        if assignment.project.manager_id == user.id:
            return True
        return assignment.user_id == user.id

    # ---------------- TASK ---------------- #

    @staticmethod
    def can_create_task(user, project):
        _validate_scope_inputs(user, project)
        if PermissionService.is_admin(user):
            return True
        return project.manager_id == user.id

    @staticmethod
    def can_create_task_for_project_id(user, project_id):
        if user is None:
            raise ValueError("User must be provided")
        if PermissionService.is_admin(user):
            return True
        return Project.objects.filter(id=project_id, manager_id=user.id).exists()

    @staticmethod
    def can_view_task_collection(user, project_id):
        if user is None:
            raise ValueError("User must be provided")
        if PermissionService.is_admin(user):
            return True
        if Project.objects.filter(id=project_id, manager_id=user.id).exists():
            return True
        return Assignment.objects.filter(
            project_id=project_id, user=user, is_active=True
        ).exists()

    @staticmethod
    def can_view_task(user, task):
        _validate_scope_inputs(user, task)
        if PermissionService.is_admin(user):
            return True
        if task.project.manager_id == user.id:
            return True
        return Assignment.objects.filter(
            project=task.project, user=user, is_active=True
        ).exists()

    @staticmethod
    def can_view_task_for_id(user, task_id):
        if user is None:
            raise ValueError("User must be provided")
        task = Task.objects.select_related("project").filter(id=task_id).only("id", "project_id", "assigned_to_id", "project__manager_id").first()
        if not task:
            return False
        return PermissionService.can_view_task(user, task)

    @staticmethod
    def can_update_task(user, task):
        _validate_scope_inputs(user, task)
        if PermissionService.is_admin(user):
            return True
        if task.project.manager_id == user.id:
            return True
        return task.assigned_to_id == user.id

    @staticmethod
    def can_update_task_for_id(user, task_id):
        if user is None:
            raise ValueError("User must be provided")
        task = Task.objects.select_related("project").filter(id=task_id).only("id", "project_id", "assigned_to_id", "project__manager_id").first()
        if not task:
            return False
        return PermissionService.can_update_task(user, task)

    @staticmethod
    def can_delete_task(user, task):
        _validate_scope_inputs(user, task)
        if PermissionService.is_admin(user):
            return True
        return task.project.manager_id == user.id

    @staticmethod
    def can_delete_task_for_id(user, task_id):
        if user is None:
            raise ValueError("User must be provided")
        if PermissionService.is_admin(user):
            return True
        return Task.objects.select_related("project").filter(id=task_id, project__manager_id=user.id).exists()

    # ---------------- AUDIT ---------------- #

    @staticmethod
    def can_view_audit_logs(user):
        _validate_scope_inputs(user, [])
        return PermissionService.is_admin(user) or PermissionService.is_manager(user) or PermissionService.is_employee(user)
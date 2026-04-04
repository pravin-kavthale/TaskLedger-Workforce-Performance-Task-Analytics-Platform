from core.permissions.services import PermissionService


def is_admin(user):
    return PermissionService.is_admin(user)

def is_manager(user):
    return PermissionService.is_manager(user)

def is_project_manager(user, project):
    return PermissionService.can_update_project(user, project)

def is_project_employee(user, project):
    return PermissionService.can_view_project(user, project)

def is_project_manager_of_project(user, project_id):
    return PermissionService.can_update_project_for_id(user, project_id)

def is_team_member(assignee, team):
    return team.members.filter(id=assignee.id).exists()

from core.permissions.services import PermissionService

def can_assign_role(request_user, target_role):
    return PermissionService.can_assign_role(request_user, target_role)
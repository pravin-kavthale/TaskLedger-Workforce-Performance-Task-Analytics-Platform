from .models import User

def can_assign_role(request_user, target_role):
    if request_user.role == User.Role.ADMIN:
        return True
    if request_user.role == User.Role.MANAGER and target_role == User.Role.EMPLOYEE:
        return True
    return False
from .models import Assignment, Project
from accounts.models import User


def is_admin(user):
    return user.role == User.Role.ADMIN

def is_project_manager(user, project):
    return (
        user.role == User.Role.MANAGER
        and project.manager_id == user.id
    )

def is_project_employee(user, project):
    return Assignment.objects.filter(
        project=project,
        user=user,
        is_active=True
    ).exists()

def is_project_manager_of_project(user, project_id):
    return Project.objects.filter(
        id=project_id,
        manager_id=user.id
    ).exists()

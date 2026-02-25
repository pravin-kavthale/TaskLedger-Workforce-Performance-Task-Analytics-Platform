from django.db import transaction
from rest_framework.exceptions import ValidationError
from accounts.models import User

def assign_user_to_team(team, user_id):
    """
    Assigns a user to a team after performing necessary validations.
    """
    if not team.is_activate:
        raise ValidationError({"team": "Cannot assign users to an inactive team."})

    try:
        user = User.objects.get(id=user_id)
    except (User.DoesNotExist, ValueError, TypeError):
        raise ValidationError({"user_id": "Target user does not exist."})

    if not user.is_active:
        raise ValidationError({"user_id": "Target user is inactive and cannot be assigned."})

    if user.department_id != team.department_id:
        raise ValidationError({"user_id": "The target user must belong to the SAME department as the team."})

    if user.team_id == team.id:
        raise ValidationError({"user_id": "The user is already assigned to this team."})

    with transaction.atomic():
        user.team = team
        user.save(update_fields=['team'])

    return user

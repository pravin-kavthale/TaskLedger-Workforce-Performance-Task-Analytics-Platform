from django.db import transaction

from .models import ActivityLog


class ActivityActionType:
    TASK_CREATED = "TASK_CREATED"
    TASK_DELETED = "TASK_DELETED"
    TASK_STATUS_CHANGED = "TASK_STATUS_CHANGED"
    TASK_ASSIGNED = "TASK_ASSIGNED"
    TASK_REASSIGNED = "TASK_REASSIGNED"
    TASK_DETAILS_UPDATED = "TASK_DETAILS_UPDATED"

    PROJECT_CREATED = "PROJECT_CREATED"
    PROJECT_UPDATED = "PROJECT_UPDATED"
    PROJECT_DELETED = "PROJECT_DELETED"

    USER_ASSIGNED_TO_PROJECT = "USER_ASSIGNED_TO_PROJECT"
    USER_REMOVED_FROM_PROJECT = "USER_REMOVED_FROM_PROJECT"
    USER_ROLE_CHANGED_IN_PROJECT = "USER_ROLE_CHANGED_IN_PROJECT"

    USER_ADDED_TO_TEAM = "USER_ADDED_TO_TEAM"
    USER_REMOVED_FROM_TEAM = "USER_REMOVED_FROM_TEAM"


class ActivityTargetType:
    TASK = "TASK"
    PROJECT = "PROJECT"
    TEAM = "TEAM"
    USER = "USER"


def log_activity(user, action_type, target_type, target_id, metadata=None):
    if not user or not getattr(user, "is_authenticated", False):
        return

    payload = metadata if isinstance(metadata, dict) else {}

    def _create_log():
        ActivityLog.objects.create(
            user=user,
            action_type=action_type,
            target_type=target_type,
            target_id=target_id,
            metadata=payload,
        )

    transaction.on_commit(_create_log)

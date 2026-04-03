from django.conf import settings
from django.db import transaction

from .metadata_validation import validate_activity_metadata
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


class ActivityLogService:
    @staticmethod
    def _normalize_metadata(metadata):
        return metadata if isinstance(metadata, dict) else {}

    @classmethod
    def _validate_for_write(cls, action_type, metadata):
        return validate_activity_metadata(
            action_type,
            metadata,
            strict=settings.DEBUG,
            mark_invalid_safe=not settings.DEBUG,
        )

    @classmethod
    def create_log(cls, *, user, action_type, target_type, target_id, metadata=None):
        if not user or not getattr(user, "is_authenticated", False):
            return None

        payload, _ = cls._validate_for_write(action_type, cls._normalize_metadata(metadata))

        return ActivityLog.objects.create(
            user=user,
            action_type=action_type,
            target_type=target_type,
            target_id=target_id,
            metadata=payload,
        )

    @classmethod
    def enqueue_log(cls, *, user, action_type, target_type, target_id, metadata=None):
        if not user or not getattr(user, "is_authenticated", False):
            return

        payload, _ = cls._validate_for_write(action_type, cls._normalize_metadata(metadata))

        def _create_log():
            cls.create_log(
                user=user,
                action_type=action_type,
                target_type=target_type,
                target_id=target_id,
                metadata=payload,
            )

        transaction.on_commit(_create_log)

    @classmethod
    def log_task_status_change(cls, *, user, task, old, new):
        return cls.enqueue_log(
            user=user,
            action_type=ActivityActionType.TASK_STATUS_CHANGED,
            target_type=ActivityTargetType.TASK,
            target_id=task.id,
            metadata={"status": {"old": old, "new": new}},
        )

    @classmethod
    def log_team_member_removed(cls, *, user, team_id, removed_user_id):
        return cls.enqueue_log(
            user=user,
            action_type=ActivityActionType.USER_REMOVED_FROM_TEAM,
            target_type=ActivityTargetType.TEAM,
            target_id=team_id,
            metadata={
                "user_id": {"old": removed_user_id, "new": None},
                "team_id": {"old": team_id, "new": team_id},
            },
        )

    @classmethod
    def log_project_assigned(cls, *, user, project_id, assigned_user_id):
        return cls.enqueue_log(
            user=user,
            action_type=ActivityActionType.USER_ASSIGNED_TO_PROJECT,
            target_type=ActivityTargetType.PROJECT,
            target_id=project_id,
            metadata={
                "user_id": {"old": None, "new": assigned_user_id},
                "project_id": {"old": None, "new": project_id},
            },
        )


def log_activity(user, action_type, target_type, target_id, metadata=None):
    ActivityLogService.enqueue_log(
        user=user,
        action_type=action_type,
        target_type=target_type,
        target_id=target_id,
        metadata=metadata,
    )

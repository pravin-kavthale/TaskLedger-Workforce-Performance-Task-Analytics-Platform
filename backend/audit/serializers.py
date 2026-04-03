from django.conf import settings
from rest_framework import serializers

from accounts.models import User

from .metadata_validation import validate_activity_metadata
from .models import ActivityLog
from .services import ActivityActionType, ActivityTargetType


class ActivityLogUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "name"]

    def get_name(self, obj):
        return (obj.username or "").strip() or obj.email


class ActivityLogSerializer(serializers.ModelSerializer):
    user = ActivityLogUserSerializer(read_only=True)
    target_display = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()

    class Meta:
        model = ActivityLog
        fields = [
            "id",
            "user",
            "action_type",
            "target_type",
            "target_id",
            "target_display",
            "message",
            "metadata",
            "created_at",
        ]

    def get_target_display(self, obj):
        cache = self.context.get("target_display_cache", {})
        target_map = cache.get(obj.target_type, {})
        return target_map.get(obj.target_id, f"{obj.target_type} #{obj.target_id}")

    def get_message(self, obj):
        user_label = self._resolve_user_label(obj.user)
        metadata = obj.metadata if isinstance(obj.metadata, dict) else {}
        try:
            return self._build_message(obj, metadata, user_label)
        except ValueError:
            if settings.DEBUG:
                raise
            return f"User performed {obj.action_type}"

    def _build_message(self, obj, metadata, user_label):
        self._validate_metadata(obj, metadata)

        if obj.action_type == ActivityActionType.TASK_STATUS_CHANGED:
            old_value, new_value = self._get_change(metadata, "status")
            return f"User {user_label} changed task status from {old_value} to {new_value}"

        if obj.action_type == ActivityActionType.TASK_ASSIGNED:
            _, new_value = self._get_change(metadata, "assigned_to")
            return f"User {user_label} assigned task to {new_value}"

        if obj.action_type == ActivityActionType.TASK_REASSIGNED:
            old_value, new_value = self._get_change(metadata, "assigned_to")
            return f"User {user_label} reassigned task from {old_value} to {new_value}"

        if obj.action_type == ActivityActionType.TASK_DETAILS_UPDATED:
            fields_changed = ", ".join(sorted(metadata.keys()))
            return f"User {user_label} updated task details ({fields_changed})"

        if obj.action_type == ActivityActionType.USER_ADDED_TO_TEAM:
            return f"User {user_label} added member to team"

        if obj.action_type == ActivityActionType.USER_REMOVED_FROM_TEAM:
            return f"User {user_label} removed member from team"

        return self._generic_message(user_label, obj.action_type, obj.target_type)

    def _validate_metadata(self, obj, metadata):
        validate_activity_metadata(obj.action_type, metadata, strict=True)

    def _raise_invalid(self, action_type, detail):
        raise ValueError(f"Invalid activity log metadata for {action_type}: {detail}")

    def _resolve_user_label(self, user):
        if not user:
            return "Unknown user"
        username = (getattr(user, "username", "") or "").strip()
        return username or user.email

    def _get_change(self, metadata, field_name):
        value = metadata.get(field_name, {}) if isinstance(metadata, dict) else {}
        if not isinstance(value, dict):
            return None, None
        old_value = value.get("old")
        new_value = value.get("new")
        return self._to_text(old_value), self._to_text(new_value)

    def _generic_message(self, user_label, action_type, target_type):
        readable_action = (action_type or "UPDATED").replace("_", " ").lower()
        readable_target = (target_type or "record").replace("_", " ").lower()
        return f"User {user_label} performed {readable_action} on {readable_target}"

    def _to_text(self, value):
        if value is None:
            return None
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)

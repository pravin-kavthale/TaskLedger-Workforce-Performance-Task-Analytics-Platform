from copy import deepcopy


EXPECTED_METADATA = {
    "TASK_STATUS_CHANGED": [
        {"path": "status.old", "required": True, "allow_none": False},
        {"path": "status.new", "required": True, "allow_none": False},
    ],
    "TASK_ASSIGNED": [
        {"path": "assigned_to", "required": True, "type": dict},
        {"path": "assigned_to.new", "required": True, "allow_none": False},
    ],
    "TASK_REASSIGNED": [
        {"path": "assigned_to", "required": True, "type": dict},
        {"path": "assigned_to.old", "required": True, "allow_none": False},
        {"path": "assigned_to.new", "required": True, "allow_none": False},
    ],
    "TASK_DETAILS_UPDATED": [
        {"path": "*", "required": True, "non_empty": True},
    ],
    "USER_ADDED_TO_TEAM": [
        {"path": "user_id", "required": True, "type": dict},
        {"path": "team_id", "required": True, "type": dict},
        {"path": "user_id.new", "required": True, "allow_none": False},
        {"path": "team_id.new", "required": True, "allow_none": False},
    ],
    "USER_REMOVED_FROM_TEAM": [
        {"path": "user_id", "required": True, "type": dict},
        {"path": "team_id", "required": True, "type": dict},
    ],
    "USER_ASSIGNED_TO_PROJECT": [
        {"path": "user_id", "required": True, "type": dict},
        {"path": "user_id.new", "required": True, "allow_none": False},
    ],
}


def _get_nested_value(payload, path):
    if not isinstance(payload, dict):
        return False, None

    node = payload
    for key in path.split("."):
        if not isinstance(node, dict) or key not in node:
            return False, None
        node = node[key]
    return True, node


def _ensure_nested_path(payload, path):
    node = payload
    keys = path.split(".")
    for key in keys[:-1]:
        child = node.get(key)
        if not isinstance(child, dict):
            child = {}
            node[key] = child
        node = child
    leaf = keys[-1]
    node.setdefault(leaf, None)


def _safe_metadata_for_invalid(metadata, rules):
    safe = deepcopy(metadata) if isinstance(metadata, dict) else {}
    for rule in rules:
        path = rule.get("path")
        if not path or path == "*":
            continue
        if rule.get("required"):
            _ensure_nested_path(safe, path)
    safe["_invalid_safe"] = True
    return safe


def validate_activity_metadata(action_type, metadata, *, strict=False, mark_invalid_safe=False):
    payload = deepcopy(metadata) if isinstance(metadata, dict) else {}
    rules = EXPECTED_METADATA.get(action_type, [])
    errors = []

    for rule in rules:
        path = rule.get("path")
        if path == "*":
            if rule.get("non_empty") and not payload:
                errors.append("expected non-empty metadata")
            continue

        exists, value = _get_nested_value(payload, path)

        if rule.get("required") and not exists:
            errors.append(f"missing required metadata path '{path}'")
            continue

        if not exists:
            continue

        if not rule.get("allow_none", True) and value is None:
            errors.append(f"metadata path '{path}' cannot be null")

        expected_type = rule.get("type")
        if expected_type and value is not None and not isinstance(value, expected_type):
            errors.append(f"metadata path '{path}' must be {expected_type.__name__}")

    if errors and strict:
        raise ValueError(f"Invalid activity log metadata for {action_type}: {'; '.join(errors)}")

    if errors and mark_invalid_safe:
        return _safe_metadata_for_invalid(payload, rules), False

    return payload, not errors

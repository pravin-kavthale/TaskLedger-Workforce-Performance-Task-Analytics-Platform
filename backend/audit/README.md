# Activity Logging System (AuditLog)

## 1. OVERVIEW

The Activity Logging System is a centralized audit trail mechanism for the TaskLedger platform. It records all significant user actions within the system to provide complete traceability, support debugging, and enable analytics functionality.

**Core Purpose:**

- Track user interactions with tasks, projects, and teams
- Maintain an immutable historical record of changes
- Enable role-based visibility of activity logs
- Support forensic analysis and compliance requirements

**Why It Exists:**

- **Traceability:** Know who did what and when
- **Debugging:** Reconstruct sequences of events leading to issues
- **Analytics:** Generate insights on platform usage and employee performance
- **Accountability:** Maintain compliance records for audits

---

## 2. ARCHITECTURE DESIGN

### Service-Oriented Approach

The Activity Logging System enforces a strict service layer pattern where **direct model writes are prohibited**. All activity must flow through the centralized `ActivityLogService`.

**Why This Pattern:**

1. **Single Responsibility:** All logging logic lives in one place, preventing scattered implementations
2. **Consistency:** Guarantees validation and metadata enforcement across all logging calls
3. **Transaction Safety:** Ensures logs are written within proper transaction boundaries
4. **Testability:** Service methods can be mocked or bypassed during testing
5. **Future Scalability:** Enables queuing, batching, or external logging without code changes

### Data Flow

```
API/View Code
    ↓
ActivityLogService.enqueue_log() or create_log()
    ↓
Metadata Normalization & Validation
    ↓
Database Write (transaction.on_commit for safety)
```

### Transaction Safety

The system uses `transaction.on_commit()` to ensure activity logs are only written after the primary transaction succeeds. This prevents orphaned logs and maintains consistency.

---

## 3. MODEL STRUCTURE

### ActivityLog Fields

| Field         | Type             | Purpose                                                 |
| ------------- | ---------------- | ------------------------------------------------------- |
| `id`          | AutoField        | Primary key                                             |
| `user`        | ForeignKey(User) | Which user performed the action                         |
| `action_type` | CharField(50)    | What action was performed (e.g., "TASK_STATUS_CHANGED") |
| `target_type` | CharField(50)    | Type of resource affected (e.g., "TASK", "PROJECT")     |
| `target_id`   | IntegerField     | ID of the affected resource                             |
| `metadata`    | JSONField        | Action-specific structured data (see Metadata System)   |
| `created_at`  | DateTimeField    | Timestamp (auto-set, immutable)                         |

**Key Characteristics:**

- Append-only: Once created, activity logs are never modified or deleted
- Indexed: `user`, `action_type`, and `created_at` are optimized for common queries
- No cascading: Logs remain even if the referenced user or resource is deleted

---

## 4. ACTION TYPES

Activity logs are categorized into structured action types using enum-like constants. This prevents typos and enables consistent filtering/reporting.

### Task Actions

- `TASK_CREATED` — Task was created
- `TASK_DELETED` — Task was deleted
- `TASK_STATUS_CHANGED` — Task status transitioned (e.g., TODO → IN_PROGRESS)
- `TASK_ASSIGNED` — Task was assigned to a user
- `TASK_REASSIGNED` — Task assignment changed to different user
- `TASK_DETAILS_UPDATED` — Task metadata (title, description, etc.) was modified

### Project Actions

- `PROJECT_CREATED` — Project was created
- `PROJECT_UPDATED` — Project settings changed
- `PROJECT_DELETED` — Project was deleted

### Team Actions

- `USER_ADDED_TO_TEAM` — User was added to a team
- `USER_REMOVED_FROM_TEAM` — User was removed from a team

### Project Membership Actions

- `USER_ASSIGNED_TO_PROJECT` — User was assigned to a project
- `USER_REMOVED_FROM_PROJECT` — User's project access was revoked
- `USER_ROLE_CHANGED_IN_PROJECT` — User's project role was modified

**Why Enums:**
Structured constants prevent invalid action types, support IDE autocomplete, and make it easy to add new actions systematically.

---

## 5. METADATA SYSTEM

### Schema-Based Validation

Metadata is validated against the `EXPECTED_METADATA` schema. This schema describes which fields are required, their types, and whether they can be null.

### Dotted Path Validation

The validation system uses dotted notation to access nested JSON paths:

```python
# Required metadata path "status.old" means:
# metadata = {"status": {"old": <value>}}
```

For example, `TASK_STATUS_CHANGED` requires:

- `status.old` — the previous status value
- `status.new` — the new status value

### Validation Modes

#### DEBUG Mode (Development)

- **Strict Validation:** Any metadata error raises `ValueError`
- **No Fallback:** Logs fail fast, forcing developers to fix issues immediately
- **Purpose:** Catch bugs during development

#### Production Mode

- **Safe Fallback:** Invalid metadata is marked and stored safely
- **No Crashes:** Metadata errors do NOT prevent log creation
- **Purpose:** Ensure logging never breaks business logic due to validation

**Example:**

```python
# In settings.DEBUG = True (strict)
metadata = {}  # Missing required "status.old"
validate_activity_metadata("TASK_STATUS_CHANGED", metadata, strict=True)
# → Raises ValueError

# In settings.DEBUG = False (safe)
metadata = {}
payload, valid = validate_activity_metadata(
    "TASK_STATUS_CHANGED", metadata, mark_invalid_safe=True
)
# → payload = {"status": {"old": None, "new": None}, "_invalid_safe": True}
# → valid = False
# Log is still created, but marked as invalid
```

---

## 6. ACTIVITY LOG SERVICE

The `ActivityLogService` provides the exclusive interface for creating activity logs. Direct model writes are forbidden.

### Class Methods

#### `create_log(user, action_type, target_type, target_id, metadata=None)`

Synchronously creates an activity log immediately.

```python
ActivityLogService.create_log(
    user=request.user,
    action_type="TASK_STATUS_CHANGED",
    target_type="TASK",
    target_id=task.id,
    metadata={"status": {"old": "TODO", "new": "DONE"}}
)
```

**Returns:** The created `ActivityLog` instance or `None` if user is unauthenticated.

#### `enqueue_log(user, action_type, target_type, target_id, metadata=None)`

Schedules log creation to occur after the current transaction commits (safe for use in views).

```python
ActivityLogService.enqueue_log(
    user=request.user,
    action_type="TASK_ASSIGNED",
    target_type="TASK",
    target_id=task.id,
    metadata={"assigned_to": {"new": assignee.id}}
)
```

**Use Case:** Called at the end of a model save signal or view to ensure the primary transaction succeeds before logging.

#### `log_task_status_change(user, task, old, new)`

Specialized helper for logging task status changes.

```python
ActivityLogService.log_task_status_change(
    user=request.user,
    task=task,
    old="TODO",
    new="IN_PROGRESS"
)
```

#### `log_team_member_removed(user, team_id, removed_user_id)`

Specialized helper for logging team member removal.

```python
ActivityLogService.log_team_member_removed(
    user=request.user,
    team_id=team.id,
    removed_user_id=removed_user.id
)
```

#### `log_project_assigned(user, project_id, assigned_user_id)`

Specialized helper for logging project assignment.

```python
ActivityLogService.log_project_assigned(
    user=request.user,
    project_id=project.id,
    assigned_user_id=user_to_assign.id
)
```

### Transaction Safety

All logging methods internally call `transaction.on_commit()` to defer writes:

```python
def enqueue_log(...):
    payload, _ = cls._validate_for_write(action_type, metadata)

    def _create_log():
        cls.create_log(user=user, action_type=action_type, ...)

    transaction.on_commit(_create_log)
```

This ensures:

1. If the primary transaction rolls back, the log is never written
2. The log is written after the primary transaction commits
3. No "ghost logs" exist for failed operations

---

## 7. SERIALIZER LOGIC

The `ActivityLogSerializer` provides human-readable output for API consumers.

### Human-Readable Messages

Messages are generated dynamically from metadata and action type:

```python
# Input:
log = ActivityLog(
    action_type="TASK_STATUS_CHANGED",
    user=User(username="Alice"),
    metadata={"status": {"old": "TODO", "new": "DONE"}}
)

# Output message:
"User Alice changed task status from TODO to DONE"
```

### Message Templates by Action Type

| Action                   | Template                                              |
| ------------------------ | ----------------------------------------------------- |
| `TASK_STATUS_CHANGED`    | "User {user} changed task status from {old} to {new}" |
| `TASK_ASSIGNED`          | "User {user} assigned task to {new}"                  |
| `TASK_REASSIGNED`        | "User {user} reassigned task from {old} to {new}"     |
| `TASK_DETAILS_UPDATED`   | "User {user} updated task details ({fields})"         |
| `USER_ADDED_TO_TEAM`     | "User {user} added member to team"                    |
| `USER_REMOVED_FROM_TEAM` | "User {user} removed member from team"                |
| (generic)                | "User {user} performed {action} on {target}"          |

### Fallback Behavior

If metadata is invalid and the serializer is in strict mode (DEBUG), an error is raised. In production, a generic message is returned:

```python
if settings.DEBUG:
    raise ValueError("Invalid metadata for TASK_ASSIGNED")
else:
    return "User Alice performed task_assigned on task"
```

### Target Display Cache

The serializer pre-caches task/project/team names to avoid N+1 queries:

```python
context = {
    "target_display_cache": {
        "TASK": {1: "Fix login bug", 2: "Build landing page"},
        "PROJECT": {1: "Project Alpha", 2: "Project Beta"},
        "TEAM": {1: "Team A", 2: "Team B"}
    }
}
```

---

## 8. PERMISSION & VISIBILITY

Role-based access control ensures users only see activity logs they should.

### Admin

```python
# Full access to all activity logs
GET /api/activity-logs/ → all logs (no filtering)
```

### Manager

```python
# Can see:
# - Logs they created personally
# - Activity on projects they manage
# - Activity on teams they manage
# - Activity on tasks in their projects/teams
GET /api/activity-logs/ → filtered results
```

### Employee

```python
# Can see:
# - Logs they created personally
# - Activity on tasks assigned to them
# - Actions involving their team/project membership changes
GET /api/activity-logs/ → filtered results
```

### Mixed-Role Handling

The system supports users with multiple roles. The visibility query dynamically combines role-specific filters:

```python
if user.role == User.Role.ADMIN:
    return self._admin_queryset(user)
elif user.role == User.Role.MANAGER:
    return self._manager_queryset(user)
elif user.role == User.Role.EMPLOYEE:
    return self._employee_queryset(user)
```

Edge case: An employee with admin role still gets admin-level access.

---

## 9. API DESIGN

### Endpoint

```
GET /api/activity-logs/
GET /api/activity-logs/{id}/
```

### Supported Filters

| Parameter         | Type     | Example                                 |
| ----------------- | -------- | --------------------------------------- |
| `user`            | integer  | `?user=5`                               |
| `action_type`     | string   | `?action_type=TASK_STATUS_CHANGED`      |
| `target_type`     | string   | `?target_type=TASK`                     |
| `target_id`       | integer  | `?target_id=10`                         |
| `created_at__gte` | ISO 8601 | `?created_at__gte=2026-01-01T00:00:00Z` |
| `created_at__lte` | ISO 8601 | `?created_at__lte=2026-12-31T23:59:59Z` |

### Search

Full-text search across:

- `action_type`
- `metadata` (JSON cast to text)
- `user__username`
- `user__email`

```
GET /api/activity-logs/?search=Alice
```

### Ordering

Default: `-created_at` (newest first)

Available fields: `created_at`, `action_type`

```
GET /api/activity-logs/?ordering=action_type
```

### Pagination

- **Page Size:** 20 items (default)
- **Max Page Size:** 100 items
- **Type:** Page number pagination

```json
{
  "count": 250,
  "next": "http://api/activity-logs/?page=2",
  "previous": null,
  "results": [...]
}
```

### Response Format

```json
{
  "id": 1,
  "user": {
    "id": 5,
    "email": "alice@example.com",
    "name": "Alice"
  },
  "action_type": "TASK_STATUS_CHANGED",
  "target_type": "TASK",
  "target_id": 42,
  "target_display": "Fix login bug",
  "message": "User Alice changed task status from TODO to DONE",
  "metadata": {
    "status": {
      "old": "TODO",
      "new": "DONE"
    }
  },
  "created_at": "2026-04-01T14:30:00Z"
}
```

---

## 10. TESTING STRATEGY

### Test Coverage

**Unit Tests:**

- Log creation with valid metadata
- Service validation modes (strict vs. safe)
- Metadata normalization (None, invalid types, etc.)

**Integration Tests:**

- End-to-end log creation flow
- Database constraints and indexing
- Transaction safety (on_commit behavior)

**API Tests:**

- Role-based filtering (admin, manager, employee)
- Pagination and search
- Mixed-role visibility edge cases

### Key Test Case: Mixed-Role Visibility

An employee assigned to multiple projects should see logs for all their assignments, even if filtered by different role logic:

```python
def test_employee_with_multiple_projects_sees_relevant_logs(self):
    # employee_user_1 is assigned to project_a
    # Log created for task_a (in project_a)
    # Employee should see this log

    logs = self._get_employee_logs(employee_user_1)
    assert self.log_task_a in logs
```

### No Direct Model Writes in Tests

Tests always use `ActivityLogService.create_log()` or `ActivityLogService.enqueue_log()` to create logs. Direct model writes (e.g., `ActivityLog.objects.create()`) are avoided to ensure test behavior matches production.

```python
# ✅ Correct
log = ActivityLogService.create_log(
    user=self.user,
    action_type="TASK_CREATED",
    target_type="TASK",
    target_id=1,
    metadata={}
)

# ❌ Avoid
log = ActivityLog.objects.create(
    user=self.user,
    action_type="TASK_CREATED",
    ...
)
```

---

## 11. DESIGN DECISIONS

### Why Service Layer?

Enforcing a service layer prevents scattered logging logic across views, signals, and serializers. This centralizes validation, makes testing easier, and allows future refactoring (e.g., external logging providers) without breaking the API.

### Why Schema-Based Metadata?

Metadata is flexible (JSON), but validation ensures consistency. A schema (`EXPECTED_METADATA`) documents what metadata fields each action requires, catching bugs early while allowing new actions to be added incrementally.

### Why Centralized Validation?

Validation logic is complex (nested paths, type checking, null handling). Centralizing it in `validate_activity_metadata()` prevents duplication and ensures the same rules apply everywhere.

### Why Async-Safe Logging (transaction.on_commit)?

Database transactions can fail (e.g., duplicate key, constraint violation). Using `transaction.on_commit()` ensures logs are only written after the primary transaction succeeds, maintaining consistency and preventing orphaned logs.

### Why Immutable Logs?

Activity logs are audit records. Making them immutable (no UPDATE, DELETE) ensures the historical record is trustworthy. If a log needs correction, the correct approach is to create a new log, not modify the old one.

---

## 12. LIMITATIONS

### No Metadata Versioning

The `EXPECTED_METADATA` schema is static. If action requirements change (e.g., adding a new required field), old logs won't have the new field. There is no mechanism to track schema version per log.

**Impact:** Reporting tools must handle missing or extra metadata gracefully.

### Basic Fallback Handling

In production, invalid metadata is marked with `_invalid_safe: True` but not quarantined. The log is still queryable, which may surface invalid data in reports.

**Impact:** Analytics queries must filter out invalid logs or handle missing fields.

### Not Optimized for Large-Scale Analytics

The current pagination is page-based (not cursor-based), and there is no analytics-specific indexing. Running queries across millions of logs may be slow.

**Impact:** Real-time analytics dashboards should use a separate OLAP system, not the operational logs table.

---

## 13. FUTURE IMPROVEMENTS

### Metadata Versioning

Track the schema version used when each log was created:

```json
{
  "metadata": {...},
  "metadata_version": "1.0"
}
```

This enables forward compatibility if the schema changes.

### Indexing Strategy

Add composite indexes for common queries:

- `(user_id, created_at DESC)`
- `(action_type, created_at DESC)`
- `(target_type, target_id, created_at DESC)`

### Analytics Layer

Implement a separate read model (e.g., materialized view, data warehouse export) optimized for analytics, separate from operational logs.

### Log Retention Policies

Implement automatic archival/deletion of logs older than N years to manage database size.

### Webhook/Event System

Support external subscribers that react to activity in real-time:

```python
signals.activity_logged.send(
    sender=ActivityLog,
    action_type="TASK_STATUS_CHANGED",
    user=user,
    target_id=task_id
)
```

### Bulk Logging API

Support batch log creation for high-volume scenarios:

```python
ActivityLogService.enqueue_logs([
    {"user": user1, "action_type": "TASK_CREATED", ...},
    {"user": user2, "action_type": "TASK_ASSIGNED", ...},
])
```

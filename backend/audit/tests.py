from datetime import date

from django.test import TestCase, override_settings
from rest_framework.test import APIRequestFactory, force_authenticate

from accounts.models import User
from organization.models import Department, Team
from work.models import Assignment, Project, Task

from .models import ActivityLog
from .serializers import ActivityLogSerializer
from .services import ActivityActionType, ActivityTargetType
from .views import ActivityLogViewSet


class ActivityLogAPITestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.department = Department.objects.create(
            name="Engineering",
            code="ENG",
            created_by=None,
        )

        self.admin = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="pass12345",
            role=User.Role.ADMIN,
        )
        self.manager = User.objects.create_user(
            username="manager",
            email="manager@test.com",
            password="pass12345",
            role=User.Role.MANAGER,
            department=self.department,
        )
        self.employee = User.objects.create_user(
            username="employee",
            email="employee@test.com",
            password="pass12345",
            role=User.Role.EMPLOYEE,
            department=self.department,
        )
        self.other_manager = User.objects.create_user(
            username="other-manager",
            email="other-manager@test.com",
            password="pass12345",
            role=User.Role.MANAGER,
            department=self.department,
        )
        self.other_employee = User.objects.create_user(
            username="other-employee",
            email="other-employee@test.com",
            password="pass12345",
            role=User.Role.EMPLOYEE,
            department=self.department,
        )

        self.team = Team.objects.create(
            name="Core Team",
            code="CORE",
            department=self.department,
            manager=self.manager,
            created_by=self.admin,
        )
        self.other_team = Team.objects.create(
            name="Other Team",
            code="OTHR",
            department=self.department,
            manager=self.other_manager,
            created_by=self.admin,
        )

        self.project = Project.objects.create(
            name="Login Revamp",
            code="PRJ-1",
            description="Improve login flow",
            team=self.team,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            department=self.department,
            created_by=self.admin,
        )
        self.other_project = Project.objects.create(
            name="Mobile App",
            code="PRJ-2",
            description="Unrelated project",
            team=self.other_team,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            department=self.department,
            created_by=self.admin,
        )

        self.assignment = Assignment.objects.create(
            project=self.project,
            user=self.employee,
            role=Assignment.Role.SOFTWARE_ENGINEER,
            assigned_by=self.manager,
            is_active=True,
        )
        self.other_assignment = Assignment.objects.create(
            project=self.other_project,
            user=self.other_employee,
            role=Assignment.Role.SOFTWARE_ENGINEER,
            assigned_by=self.other_manager,
            is_active=True,
        )

        self.task = Task.objects.create(
            project=self.project,
            assigned_to=self.employee,
            title="Fix login bug",
            description="Handle token refresh",
            priority=Task.Priority.HIGH,
            estimated_hours=5,
            created_by=self.manager,
            status=Task.Status.TODO,
        )
        self.other_task = Task.objects.create(
            project=self.other_project,
            assigned_to=self.other_employee,
            title="Build landing page",
            description="Marketing content",
            priority=Task.Priority.MEDIUM,
            estimated_hours=3,
            created_by=self.other_manager,
            status=Task.Status.TODO,
        )

        self.project_log = ActivityLog.objects.create(
            user=self.manager,
            action_type=ActivityActionType.PROJECT_UPDATED,
            target_type=ActivityTargetType.PROJECT,
            target_id=self.project.id,
            metadata={"name": {"old": "Login", "new": "Login Revamp"}},
        )
        self.team_log = ActivityLog.objects.create(
            user=self.manager,
            action_type=ActivityActionType.USER_ADDED_TO_TEAM,
            target_type=ActivityTargetType.TEAM,
            target_id=self.team.id,
            metadata={
                "user_id": {"old": None, "new": self.employee.id},
                "team_id": {"old": None, "new": self.team.id},
            },
        )
        self.task_log = ActivityLog.objects.create(
            user=self.manager,
            action_type=ActivityActionType.TASK_STATUS_CHANGED,
            target_type=ActivityTargetType.TASK,
            target_id=self.task.id,
            metadata={"status": {"old": "TODO", "new": "DONE"}},
        )
        self.employee_log = ActivityLog.objects.create(
            user=self.employee,
            action_type=ActivityActionType.TASK_ASSIGNED,
            target_type=ActivityTargetType.TASK,
            target_id=self.task.id,
            metadata={"assigned_to": {"old": None, "new": self.employee.id}},
        )
        self.unrelated_log = ActivityLog.objects.create(
            user=self.other_manager,
            action_type=ActivityActionType.PROJECT_UPDATED,
            target_type=ActivityTargetType.PROJECT,
            target_id=self.other_project.id,
            metadata={"status": {"old": "PLANNED", "new": "ACTIVE"}},
        )

    def _list_as(self, user):
        request = self.factory.get("/api/activity-logs/")
        force_authenticate(request, user=user)
        response = ActivityLogViewSet.as_view({"get": "list"})(request)
        return response

    def test_admin_sees_all_logs(self):
        response = self._list_as(self.admin)
        self.assertEqual(response.status_code, 200)
        returned_ids = {item["id"] for item in response.data["results"]}
        self.assertIn(self.project_log.id, returned_ids)
        self.assertIn(self.team_log.id, returned_ids)
        self.assertIn(self.task_log.id, returned_ids)
        self.assertIn(self.employee_log.id, returned_ids)
        self.assertIn(self.unrelated_log.id, returned_ids)

    def test_manager_sees_only_relevant_logs(self):
        response = self._list_as(self.manager)
        self.assertEqual(response.status_code, 200)
        returned_ids = {item["id"] for item in response.data["results"]}
        self.assertIn(self.project_log.id, returned_ids)
        self.assertIn(self.team_log.id, returned_ids)
        self.assertIn(self.task_log.id, returned_ids)
        self.assertIn(self.employee_log.id, returned_ids)
        self.assertNotIn(self.unrelated_log.id, returned_ids)

    def test_employee_sees_self_and_involved_logs_only(self):
        response = self._list_as(self.employee)
        self.assertEqual(response.status_code, 200)
        returned_ids = {item["id"] for item in response.data["results"]}
        self.assertIn(self.employee_log.id, returned_ids)
        self.assertIn(self.task_log.id, returned_ids)
        self.assertIn(self.team_log.id, returned_ids)
        self.assertNotIn(self.unrelated_log.id, returned_ids)

    def test_target_display_resolves_title(self):
        request = self.factory.get(f"/api/activity-logs/{self.task_log.id}/")
        force_authenticate(request, user=self.admin)
        response = ActivityLogViewSet.as_view({"get": "retrieve"})(request, pk=self.task_log.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["target_display"], self.task.title)

    @override_settings(DEBUG=True)
    def test_invalid_metadata_raises_in_debug(self):
        bad_log = ActivityLog(
            user=self.manager,
            action_type=ActivityActionType.TASK_STATUS_CHANGED,
            target_type=ActivityTargetType.TASK,
            target_id=self.task.id,
            metadata={"status": {"old": "TODO"}},
        )
        serializer = ActivityLogSerializer(instance=bad_log)
        with self.assertRaises(ValueError):
            serializer.data

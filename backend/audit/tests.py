from datetime import timedelta

from django.test import override_settings
from django.test.utils import CaptureQueriesContext
from django.db import connection
from django.utils import timezone
from rest_framework.test import APITestCase

from accounts.models import User
from audit.models import ActivityLog
from audit.serializers import ActivityLogSerializer
from audit.services import ActivityActionType, ActivityLogService, ActivityTargetType
from organization.models import Department, Team
from work.models import Assignment, Project, Task


class ActivityLogAPITests(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name="Engineering",
            code="ENG",
            created_by=None,
        )

        self.admin_user = User.objects.create_user(
            username="admin_user",
            email="admin@test.com",
            password="pass12345",
            role=User.Role.ADMIN,
        )
        self.manager_user = User.objects.create_user(
            username="manager_user",
            email="manager@test.com",
            password="pass12345",
            role=User.Role.MANAGER,
            department=self.department,
        )
        self.other_manager = User.objects.create_user(
            username="other_manager",
            email="other-manager@test.com",
            password="pass12345",
            role=User.Role.MANAGER,
            department=self.department,
        )
        self.employee_user_1 = User.objects.create_user(
            username="employee_user_1",
            email="employee1@test.com",
            password="pass12345",
            role=User.Role.EMPLOYEE,
            department=self.department,
        )
        self.employee_user_2 = User.objects.create_user(
            username="employee_user_2",
            email="employee2@test.com",
            password="pass12345",
            role=User.Role.EMPLOYEE,
            department=self.department,
        )

        self.team_a = Team.objects.create(
            name="Team A",
            code="TEAM-A",
            department=self.department,
            manager=self.manager_user,
            created_by=self.admin_user,
        )
        self.team_b = Team.objects.create(
            name="Team B",
            code="TEAM-B",
            department=self.department,
            manager=self.other_manager,
            created_by=self.admin_user,
        )

        self.project_a = Project.objects.create(
            name="Project Alpha",
            code="PROJ-A",
            description="Project A",
            team=self.team_a,
            start_date="2026-01-01",
            end_date="2026-12-31",
            department=self.department,
            created_by=self.admin_user,
        )
        self.project_b = Project.objects.create(
            name="Project Beta",
            code="PROJ-B",
            description="Project B",
            team=self.team_b,
            start_date="2026-01-01",
            end_date="2026-12-31",
            department=self.department,
            created_by=self.admin_user,
        )

        self.assignment_a = Assignment.objects.create(
            project=self.project_a,
            user=self.employee_user_1,
            role=Assignment.Role.SOFTWARE_ENGINEER,
            assigned_by=self.manager_user,
            is_active=True,
        )
        self.assignment_b = Assignment.objects.create(
            project=self.project_b,
            user=self.employee_user_2,
            role=Assignment.Role.SOFTWARE_ENGINEER,
            assigned_by=self.other_manager,
            is_active=True,
        )

        self.task_a = Task.objects.create(
            project=self.project_a,
            assigned_to=self.employee_user_1,
            title="Fix login bug",
            description="Handle token refresh",
            priority=Task.Priority.HIGH,
            estimated_hours=5,
            created_by=self.manager_user,
            status=Task.Status.TODO,
        )
        self.task_b = Task.objects.create(
            project=self.project_b,
            assigned_to=self.employee_user_2,
            title="Build landing page",
            description="Marketing content",
            priority=Task.Priority.MEDIUM,
            estimated_hours=3,
            created_by=self.other_manager,
            status=Task.Status.TODO,
        )

        self.log_task_a = ActivityLogService.create_log(
            user=self.employee_user_1,
            action_type=ActivityActionType.TASK_STATUS_CHANGED,
            target_type=ActivityTargetType.TASK,
            target_id=self.task_a.id,
            metadata={"status": {"old": "TODO", "new": "DONE"}},
        )
        self.log_task_b = ActivityLogService.create_log(
            user=self.other_manager,
            action_type=ActivityActionType.TASK_STATUS_CHANGED,
            target_type=ActivityTargetType.TASK,
            target_id=self.task_b.id,
            metadata={"status": {"old": "TODO", "new": "DONE"}},
        )
        self.log_team_a = ActivityLogService.create_log(
            user=self.manager_user,
            action_type=ActivityActionType.USER_ADDED_TO_TEAM,
            target_type=ActivityTargetType.TEAM,
            target_id=self.team_a.id,
            metadata={
                "user_id": {"old": None, "new": self.employee_user_1.id},
                "team_id": {"old": None, "new": self.team_a.id},
            },
        )
        self.log_team_b = ActivityLogService.create_log(
            user=self.other_manager,
            action_type=ActivityActionType.USER_REMOVED_FROM_TEAM,
            target_type=ActivityTargetType.TEAM,
            target_id=self.team_b.id,
            metadata={
                "user_id": {"old": self.employee_user_2.id, "new": None},
                "team_id": {"old": self.team_b.id, "new": self.team_b.id},
            },
        )
        self.log_project_a = ActivityLogService.create_log(
            user=self.manager_user,
            action_type=ActivityActionType.PROJECT_CREATED,
            target_type=ActivityTargetType.PROJECT,
            target_id=self.project_a.id,
            metadata={"name": {"old": None, "new": self.project_a.name}},
        )
        self.log_project_b = ActivityLogService.create_log(
            user=self.other_manager,
            action_type=ActivityActionType.PROJECT_CREATED,
            target_type=ActivityTargetType.PROJECT,
            target_id=self.project_b.id,
            metadata={"name": {"old": None, "new": self.project_b.name}},
        )

    def _login(self, user):
        self.client.force_authenticate(user=user)

    def _get_list(self, params=None):
        return self.client.get("/api/activity-logs/", data=params or {})

    def _get_detail(self, log_id):
        return self.client.get(f"/api/activity-logs/{log_id}/")

    def _result_ids(self, response):
        results = response.data.get("results", response.data)
        return {item["id"] for item in results}

    def test_admin_sees_all_logs(self):
        self._login(self.admin_user)
        response = self._get_list()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 6)
        self.assertSetEqual(
            self._result_ids(response),
            {
                self.log_task_a.id,
                self.log_task_b.id,
                self.log_team_a.id,
                self.log_team_b.id,
                self.log_project_a.id,
                self.log_project_b.id,
            },
        )

    def test_manager_sees_only_relevant_project_and_team_logs(self):
        self._login(self.manager_user)
        response = self._get_list()
        self.assertEqual(response.status_code, 200)
        returned_ids = self._result_ids(response)
        self.assertIn(self.log_task_a.id, returned_ids)
        self.assertIn(self.log_team_a.id, returned_ids)
        self.assertIn(self.log_project_a.id, returned_ids)
        self.assertNotIn(self.log_task_b.id, returned_ids)
        self.assertNotIn(self.log_team_b.id, returned_ids)
        self.assertNotIn(self.log_project_b.id, returned_ids)

    def test_employee_sees_self_and_involved_logs_only(self):
        self._login(self.employee_user_1)
        response = self._get_list()
        self.assertEqual(response.status_code, 200)
        returned_ids = self._result_ids(response)
        self.assertIn(self.log_task_a.id, returned_ids)
        self.assertIn(self.log_team_a.id, returned_ids)
        self.assertIn(self.log_task_a.id, returned_ids)
        self.assertNotIn(self.log_task_b.id, returned_ids)
        self.assertNotIn(self.log_team_b.id, returned_ids)
        self.assertNotIn(self.log_project_a.id, returned_ids)
        self.assertNotIn(self.log_project_b.id, returned_ids)

    def test_employee_cannot_access_project_b_logs(self):
        self._login(self.employee_user_1)
        response = self._get_list({"target_type": "PROJECT", "target_id": self.project_b.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])

    def test_mixed_role_manager_visibility_has_no_overexposure_or_duplicates(self):
        Assignment.objects.create(
            project=self.project_b,
            user=self.manager_user,
            role=Assignment.Role.SOFTWARE_ENGINEER,
            assigned_by=self.other_manager,
            is_active=True,
        )
        task_b_for_manager = Task.objects.create(
            project=self.project_b,
            assigned_to=self.manager_user,
            title="Cross-team support task",
            description="Temporary support",
            priority=Task.Priority.MEDIUM,
            estimated_hours=2,
            created_by=self.other_manager,
            status=Task.Status.TODO,
        )
        hidden_log = ActivityLogService.create_log(
            user=self.other_manager,
            action_type=ActivityActionType.TASK_STATUS_CHANGED,
            target_type=ActivityTargetType.TASK,
            target_id=task_b_for_manager.id,
            metadata={"status": {"old": "TODO", "new": "DONE"}},
        )

        self._login(self.manager_user)
        response = self._get_list()
        self.assertEqual(response.status_code, 200)
        results = response.data["results"]
        returned_ids = [item["id"] for item in results]

        self.assertEqual(len(returned_ids), len(set(returned_ids)))
        self.assertIn(self.log_project_a.id, returned_ids)
        self.assertIn(self.log_team_a.id, returned_ids)
        self.assertNotIn(self.log_project_b.id, returned_ids)
        self.assertNotIn(self.log_team_b.id, returned_ids)
        self.assertNotIn(hidden_log.id, returned_ids)

    def test_target_display_resolves_task_and_project_names(self):
        self._login(self.admin_user)
        task_response = self._get_detail(self.log_task_a.id)
        project_response = self._get_detail(self.log_project_a.id)
        self.assertEqual(task_response.status_code, 200)
        self.assertEqual(project_response.status_code, 200)
        self.assertEqual(task_response.data["target_display"], self.task_a.title)
        self.assertEqual(project_response.data["target_display"], self.project_a.name)

    def test_target_display_falls_back_when_object_missing(self):
        self.task_a.delete()
        self._login(self.admin_user)
        response = self._get_detail(self.log_task_a.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["target_display"], f"TASK #{self.log_task_a.target_id}")

    @override_settings(DEBUG=True)
    def test_valid_task_status_message_is_human_readable(self):
        serializer = ActivityLogSerializer(instance=self.log_task_a)
        self.assertEqual(
            serializer.data["message"],
            "User employee_user_1 changed task status from TODO to DONE",
        )

    @override_settings(DEBUG=True)
    def test_invalid_metadata_raises_value_error_in_debug(self):
        invalid_log = ActivityLog(
            user=self.employee_user_1,
            action_type=ActivityActionType.TASK_STATUS_CHANGED,
            target_type=ActivityTargetType.TASK,
            target_id=self.task_a.id,
            metadata={"status": {"old": "TODO"}},
        )
        with self.assertRaises(ValueError):
            ActivityLogSerializer(instance=invalid_log).data

    @override_settings(DEBUG=False)
    def test_invalid_metadata_falls_back_in_production(self):
        invalid_log = ActivityLog(
            user=self.employee_user_1,
            action_type=ActivityActionType.TASK_STATUS_CHANGED,
            target_type=ActivityTargetType.TASK,
            target_id=self.task_a.id,
            metadata={"status": {"old": "TODO"}},
        )
        serializer = ActivityLogSerializer(instance=invalid_log)
        self.assertEqual(serializer.data["message"], "User performed TASK_STATUS_CHANGED")

    def test_filtering_by_action_type_user_and_target_type(self):
        self._login(self.admin_user)

        response = self._get_list({"action_type": ActivityActionType.TASK_STATUS_CHANGED})
        self.assertEqual(response.status_code, 200)
        returned_ids = self._result_ids(response)
        self.assertIn(self.log_task_a.id, returned_ids)
        self.assertIn(self.log_task_b.id, returned_ids)
        self.assertNotIn(self.log_project_a.id, returned_ids)

        response = self._get_list({"user": self.manager_user.id})
        returned_ids = self._result_ids(response)
        self.assertIn(self.log_team_a.id, returned_ids)
        self.assertIn(self.log_project_a.id, returned_ids)
        self.assertNotIn(self.log_task_b.id, returned_ids)

        response = self._get_list({"target_type": ActivityTargetType.TASK})
        returned_ids = self._result_ids(response)
        self.assertIn(self.log_task_a.id, returned_ids)
        self.assertIn(self.log_task_b.id, returned_ids)
        self.assertNotIn(self.log_team_a.id, returned_ids)

    def test_filtering_by_created_at_range_and_combination(self):
        self._login(self.admin_user)
        now = timezone.now()

        response = self._get_list(
            {
                "created_at__gte": (now - timedelta(minutes=1)).isoformat(),
                "created_at__lte": (now + timedelta(minutes=1)).isoformat(),
                "action_type": ActivityActionType.PROJECT_CREATED,
                "target_type": ActivityTargetType.PROJECT,
            }
        )
        self.assertEqual(response.status_code, 200)
        returned_ids = self._result_ids(response)
        self.assertIn(self.log_project_a.id, returned_ids)
        self.assertIn(self.log_project_b.id, returned_ids)
        self.assertNotIn(self.log_task_a.id, returned_ids)

    def test_search_by_action_type_and_metadata(self):
        self._login(self.admin_user)

        response = self._get_list({"search": "TASK_STATUS_CHANGED"})
        self.assertEqual(response.status_code, 200)
        returned_ids = self._result_ids(response)
        self.assertIn(self.log_task_a.id, returned_ids)
        self.assertIn(self.log_task_b.id, returned_ids)

        response = self._get_list({"search": "TODO"})
        self.assertEqual(response.status_code, 200)
        returned_ids = self._result_ids(response)
        self.assertIn(self.log_task_a.id, returned_ids)
        self.assertIn(self.log_task_b.id, returned_ids)

    def test_pagination_returns_twenty_results_and_next_page(self):
        for index in range(25):
            ActivityLogService.create_log(
                user=self.admin_user,
                action_type=ActivityActionType.TASK_DETAILS_UPDATED,
                target_type=ActivityTargetType.TASK,
                target_id=self.task_a.id,
                metadata={"description": {"old": f"old-{index}", "new": f"new-{index}"}},
            )

        self._login(self.admin_user)
        response = self._get_list()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 20)
        self.assertIsNotNone(response.data["next"])

    def test_list_query_count_stays_reasonable(self):
        self._login(self.admin_user)
        with CaptureQueriesContext(connection) as context:
            response = self._get_list()
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(context.captured_queries), 10)

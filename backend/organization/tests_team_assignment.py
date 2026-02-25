from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from organization.models import Department, Team

class TeamAssignmentTests(APITestCase):
    def setUp(self):
        # Create Departments
        self.dept_eng = Department.objects.create(name="Engineering", code="ENG")
        self.dept_hr = Department.objects.create(name="Human Resources", code="HR")

        # Create Users
        self.admin = User.objects.create_user(
            email="admin@test.com", username="admin", password="password", role=User.Role.ADMIN
        )
        self.manager1 = User.objects.create_user(
            email="manager1@test.com", username="manager1", password="password",
            role=User.Role.MANAGER, department=self.dept_eng
        )
        self.manager2 = User.objects.create_user(
            email="manager2@test.com", username="manager2", password="password",
            role=User.Role.MANAGER, department=self.dept_hr
        )
        self.employee_eng = User.objects.create_user(
            email="emp_eng@test.com", username="emp_eng", password="password",
            role=User.Role.EMPLOYEE, department=self.dept_eng
        )
        self.employee_hr = User.objects.create_user(
            email="emp_hr@test.com", username="emp_hr", password="password",
            role=User.Role.EMPLOYEE, department=self.dept_hr
        )
        self.other_employee = User.objects.create_user(
            email="other@test.com", username="other", password="password",
            role=User.Role.EMPLOYEE, department=self.dept_eng
        )

        # Create Teams
        self.team_eng = Team.objects.create(
            name="Team Eng", code="TENG", department=self.dept_eng, manager=self.manager1, created_by=self.admin
        )
        self.team_hr = Team.objects.create(
            name="Team HR", code="THR", department=self.dept_hr, manager=self.manager2, created_by=self.admin
        )

        self.url_eng = reverse('team-assign-user', kwargs={'pk': self.team_eng.id})

    def test_admin_can_assign(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url_eng, {"user_id": self.employee_eng.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.employee_eng.refresh_from_db()
        self.assertEqual(self.employee_eng.team, self.team_eng)

    def test_correct_manager_can_assign(self):
        self.client.force_authenticate(user=self.manager1)
        response = self.client.post(self.url_eng, {"user_id": self.employee_eng.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.employee_eng.refresh_from_db()
        self.assertEqual(self.employee_eng.team, self.team_eng)

    def test_wrong_manager_gets_403(self):
        self.client.force_authenticate(user=self.manager2)
        response = self.client.post(self.url_eng, {"user_id": self.employee_eng.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_gets_403(self):
        self.client.force_authenticate(user=self.other_employee)
        response = self.client.post(self.url_eng, {"user_id": self.employee_eng.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_department_mismatch_returns_400(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url_eng, {"user_id": self.employee_hr.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("SAME department", str(response.data))

    def test_duplicate_assignment_returns_400(self):
        self.employee_eng.team = self.team_eng
        self.employee_eng.save()

        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url_eng, {"user_id": self.employee_eng.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already assigned", str(response.data))

    def test_user_not_found_returns_400(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url_eng, {"user_id": 99999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not exist", str(response.data))

    def test_inactive_team_returns_400(self):
        self.team_eng.is_activate = False
        self.team_eng.save()
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url_eng, {"user_id": self.employee_eng.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("inactive team", str(response.data))

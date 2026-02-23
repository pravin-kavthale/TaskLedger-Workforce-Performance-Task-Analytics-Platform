from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from work.models import Project, Task, Assignment
from organization.models import Department, Team

class TaskPermissionTests(APITestCase):
    def setUp(self):
        # Create Department
        self.dept = Department.objects.create(name="Engineering", code="ENG")

        # Create Users
        self.admin = User.objects.create_user(email="admin@test.com", username="admin", password="password", role=User.Role.ADMIN)
        self.manager = User.objects.create_user(email="manager@test.com", username="manager", password="password", role=User.Role.MANAGER)
        self.employee1 = User.objects.create_user(email="emp1@test.com", username="emp1", password="password", role=User.Role.EMPLOYEE)
        self.employee2 = User.objects.create_user(email="emp2@test.com", username="emp2", password="password", role=User.Role.EMPLOYEE)
        self.other_user = User.objects.create_user(email="other@test.com", username="other", password="password", role=User.Role.EMPLOYEE)

        # Create Team
        self.team = Team.objects.create(name="Team A", code="TA", department=self.dept, manager=self.manager)

        # Create Project
        self.project = Project.objects.create(
            name="Project 1",
            code="P1",
            team=self.team,
            manager=self.manager,
            department=self.dept,
            start_date="2023-01-01",
            created_by=self.admin
        )

        # Assign employees to project
        Assignment.objects.create(project=self.project, user=self.employee1, role="SOFTWARE_ENGINEER")
        Assignment.objects.create(project=self.project, user=self.employee2, role="SOFTWARE_ENGINEER")

        # Create Task
        self.task = Task.objects.create(
            project=self.project,
            title="Task 1",
            assigned_to=self.employee1,
            created_by=self.admin
        )

        self.list_url = reverse('project-tasks-list', kwargs={'project_pk': self.project.id})
        self.detail_url = reverse('project-tasks-detail', kwargs={'project_pk': self.project.id, 'pk': self.task.id})

    def test_unauthenticated_no_access(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_full_access(self):
        self.client.force_authenticate(user=self.admin)

        # List
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Create
        response = self.client.post(self.list_url, {'title': 'New Task', 'project': self.project.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Update
        response = self.client.patch(self.detail_url, {'title': 'Updated Title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_pm_full_access(self):
        self.client.force_authenticate(user=self.manager)

        # List
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Create
        response = self.client.post(self.list_url, {'title': 'PM Task', 'project': self.project.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Update
        response = self.client.patch(self.detail_url, {'title': 'PM Updated Title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_assigned_member_access(self):
        self.client.force_authenticate(user=self.employee1)

        # Retrieve
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Partial Update (status) - OK
        response = self.client.patch(self.detail_url, {'status': 'IN_PROGRESS'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Reassign - Forbidden
        response = self.client.patch(self.detail_url, {'assigned_to': self.employee2.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Delete - Forbidden
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Create - Forbidden
        response = self.client.post(self.list_url, {'title': 'Emp Task', 'project': self.project.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_project_member_access(self):
        self.client.force_authenticate(user=self.employee2)

        # Retrieve
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update - Forbidden
        response = self.client.patch(self.detail_url, {'status': 'DONE'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Delete - Forbidden
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_project_member_no_access(self):
        self.client.force_authenticate(user=self.other_user)

        # List - Empty (due to get_queryset) or Forbidden?
        # has_permission should return False if not member.
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Retrieve - Forbidden
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

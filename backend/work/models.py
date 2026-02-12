# Projects, Task, assignments, deadlines, statuses

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q

# Create your models here.

class Project(models.Model):
    class Status(models.TextChoices):
        PLANNED = "PLANNED", "Planned"
        ACTIVE = "ACTIVE", "Active"
        ON_HOLD = "ON_HOLD", "On Hold"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    name=models.CharField(max_length=200)
    code=models.CharField(max_length=50, unique=True)
    description=models.TextField(blank=True, null=True)
    team = models.ForeignKey('organization.Team', on_delete=models.SET_NULL,null=True, related_name='projects')

    start_date=models.DateField()
    end_date=models.DateField(blank=True, null=True)

    manager=models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='managed_projects')
    department=models.ForeignKey('organization.Department', on_delete=models.SET_NULL, null=True, related_name='projects')
    created_by=models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='projects_created')

    status=models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['status']),
        ]
    
    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "End date cannot be earlier than start date."})
        if self.team and self.department:
            if self.team.department_id != self.department_id:
                raise ValidationError({"team": "Selected team does not belong to the specified department."})
    
    def __str__(self):
        return f"{self.name} ({self.code})"

    def save(self, *args, **kwargs):
        if self.team:
            if not self.team.manager:
                raise ValidationError("Team must have a manager.")
            self.manager = self.team.manager
        self.full_clean()
        super().save(*args, **kwargs)

class Assignment(models.Model):
    class Role(models.TextChoices):
        PROJECT_MANAGER = "PROJECT_MANAGER", "Project Manager"
        TECH_LEAD = "TECH_LEAD", "Tech Lead"
        PRODUCT_OWNER = "PRODUCT_OWNER", "Product Owner"

        SOFTWARE_ENGINEER = "SOFTWARE_ENGINEER", "Software Engineer"
        BACKEND_ENGINEER = "BACKEND_ENGINEER", "Backend Engineer"
        FRONTEND_ENGINEER = "FRONTEND_ENGINEER", "Frontend Engineer"
        DATA_ENGINEER = "DATA_ENGINEER", "Data Engineer"
        ML_ENGINEER = "ML_ENGINEER", "ML Engineer"
        DEVOPS_ENGINEER = "DEVOPS_ENGINEER", "DevOps Engineer"

        QA_ENGINEER = "QA_ENGINEER", "QA Engineer"
        QA_LEAD = "QA_LEAD", "QA Lead"
        SECURITY_ENGINEER = "SECURITY_ENGINEER", "Security Engineer"

        UI_UX_DESIGNER = "UI_UX_DESIGNER", "UI/UX Designer"
        BUSINESS_ANALYST = "BUSINESS_ANALYST", "Business Analyst"

        SYSTEM_ADMIN = "SYSTEM_ADMIN", "System Administrator"
        SUPPORT_ENGINEER = "SUPPORT_ENGINEER", "Support Engineer"
        INTERN = "INTERN", "Intern"
        CONSULTANT = "CONSULTANT", "Consultant"

    project = models.ForeignKey('work.Project',on_delete=models.CASCADE,related_name='assignments')
    user = models.ForeignKey('accounts.User',on_delete=models.CASCADE,related_name='assignments')
    role = models.CharField(max_length=30, choices=Role.choices)

    assigned_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='assignments_made')
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "user"],
                condition=models.Q(is_active=True),
                name="unique_active_assignment_per_user_per_project"
            )
        ]

        indexes = [
            models.Index(
                fields=["project"],
                condition=Q(is_active=True),
                name="active_assignment_per_proj_idx",
            ),
            models.Index(
                fields=["user"],
                condition=Q(is_active=True),
                name="active_assignment_per_user_idx",
            ),
        ]


    def __str__(self):
        return f"{self.user} → {self.project} ({self.role})"

class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "TODO", "To Do"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        REVIEW = "REVIEW", "Review"
        DONE = "DONE", "Done"
        BLOCKED = "BLOCKED", "Blocked"
    STATUS_ORDER = {
        Status.TODO: 1,
        Status.IN_PROGRESS: 2,
        Status.REVIEW: 3,
        Status.BLOCKED: 4,
        Status.DONE: 5,
    }
    class Priority(models.IntegerChoices):
        HIGH = 1, "High"
        MEDIUM = 2, "Medium"
        LOW = 3, "Low"
        
    

    project = models.ForeignKey('work.Project', on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='tasks_assigned')
    title = models.CharField(max_length = 200, blank=False)
    description = models.TextField(blank=True, null=True)
    priority = models.PositiveSmallIntegerField(choices=Priority.choices, default=Priority.LOW)  # 1-High, 2-Medium, 3-Low
    estimated_hours = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='tasks_created')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)

    status_order = models.PositiveSmallIntegerField(
        editable=False,
        db_index=True
    )
    class Meta:
        ordering = ['status_order', '-priority', '-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        

        indexes = [
        models.Index(fields=['project']),
        models.Index(fields=['assigned_to']),
    ]

    def __str__(self):
        return f"{self.title} ({self.project.code})"

    def save(self, *args, **kwargs):
        self.status_order = self.STATUS_ORDER[self.status]
        super().save(*args, **kwargs)


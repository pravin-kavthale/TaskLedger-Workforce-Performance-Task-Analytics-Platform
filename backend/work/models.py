# Projects, Task, assignments, deadlines, statuses

from django.db import models
from django.core.exceptions import ValidationError

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
    
    def __str__(self):
        return f"{self.name} ({self.code})"

    def save(self, *args, **kwargs):
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

    assigned_at = models.DateTimeField(auto_now_add=True)
    unassigned_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'user'],
                condition=models.Q(is_active=True),
                name='unique_active_assignment_per_user_per_project'
            )
        ]
        indexes = [
            models.Index(fields=['project', 'is_active']),
            models.Index(fields=['user', 'is_active']),
        ]

    def clean(self):
        if not self.is_active and not self.unassigned_at:
            raise ValidationError(
                "Inactive assignments must have unassigned_at set."
            )

    def __str__(self):
        return f"{self.user} → {self.project} ({self.role})"


    def save(self, *args, **kwargs):
        if self.unassigned_at and self.is_active:
            self.is_active = False
        self.full_clean()
        super().save(*args, **kwargs)
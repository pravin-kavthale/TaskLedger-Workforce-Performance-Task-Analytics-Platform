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


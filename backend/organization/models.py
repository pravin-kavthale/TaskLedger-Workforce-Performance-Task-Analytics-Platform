# departments,teams,structures
from django.db import models

from accounts.models import User

class Department(models.Model):
    name=models.CharField(max_length=100,unique=True)
    code=models.CharField(max_length=20,unique=True)
    description=models.TextField(blank=True,null=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey('accounts.User',on_delete=models.SET_NULL,null=True,related_name='departments_created')

    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="teams"
    )

    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="managed_teams"
    )

    members = models.ManyToManyField(
        User,
        related_name="teams"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    is_activate = models.BooleanField(default=True)



    
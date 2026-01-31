from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin

class User(AbstractUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN="ADMIN","Admin"
        MANAGER="MANAGER","Manager"
        EMPLOYEE="EMPLOYEE","Employee"
    
    email=models.EmailField(unique=True)
    role=models.CheckConstraint(max_length=20, choices=Role.choices,default='EMPLOYEE')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
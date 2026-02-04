from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin

class User(AbstractUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN="ADMIN","Admin"
        MANAGER="MANAGER","Manager"
        EMPLOYEE="EMPLOYEE","Employee"
    
    email=models.EmailField(unique=True)
    role=models.CharField(max_length=20, choices=Role.choices,default='EMPLOYEE')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_users')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    department=models.ForeignKey('organization.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
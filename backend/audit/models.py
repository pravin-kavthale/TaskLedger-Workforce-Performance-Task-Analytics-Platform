# logs, activity tracking

from django.db import models

from accounts.models import User

# Create your models here

class ActivityLog(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50)
    target_type = models.CharField(max_length=50)  
    target_id = models.IntegerField()
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return super().__str__()


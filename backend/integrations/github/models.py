from django.conf import settings
from django.db import models

class GitHubIntegration(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='github_integration')

    github_user_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255)

    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)

    token_type = models.CharField(max_length=50)
    scope = models.CharField(max_length=255,blank=True)

    expires_at = models.DateTimeField(null=True, blank=True)
    refresh_token_expires_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "integration_github_accounts"

    def __str__(self):
        return f"{self.username} ({self.user_id})"

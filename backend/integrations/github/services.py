from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from .models import GitHubIntegration
from .client import GitHubOAuthClient


class GitHubService:

    @staticmethod
    @transaction.atomic
    def connect_github(user, code):

        # Step 1: Exchange code for access token
        token_data = GitHubOAuthClient.exchange_code_for_token(code)

        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        expires_in = token_data.get("expires_in")
        token_type = token_data.get("token_type")
        scope = token_data.get("scope", "")

        if not access_token:
            raise ValidationError("failed_to_obtain_access_token")

        # Step 2: Fetch GitHub user
        github_user = GitHubOAuthClient.fetch_user(access_token)

        github_user_id = github_user.get("id")
        if not github_user_id:
            raise ValidationError("failed_to_fetch_github_user")

        username = github_user.get("login")

        # Step 3: Prevent linking same GitHub account to different users
        if GitHubIntegration.objects.filter(
            github_user_id=github_user_id
        ).exclude(user=user).exists():
            raise ValidationError("This GitHub account is already linked to another user.")

        # Step 4: Calculate expiry
        expires_at = None
        if expires_in:
            expires_at = timezone.now() + timedelta(seconds=expires_in)

        # Step 5: Save or update
        GitHubIntegration.objects.update_or_create(
            user=user,
            defaults={
                "github_user_id": github_user_id,
                "username": username,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": token_type,
                "scope": scope,
                "expires_at": expires_at,
            },
        )

        return True
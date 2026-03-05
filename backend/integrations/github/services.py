from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from .models import GitHubAccount
from .client import GitHubOAuthClient


class GitHubService:
    @staticmethod
    @transaction.atomic#- This is Critical Because this  method calls external API, Writes to DB, IF something fails halfway through, we don’t want partial state.
                        #- atomic() ensures either everything succeeds OR nothing is saved
    def connect_github(user,code):
        
        #step 1: exchange code for access token
        token_data = GitHubOAuthClient.exchange_code_for_token(code)
        #Extracting Token Fields
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')
        expires_in = token_data.get('expires_in')
        token_type = token_data.get('token_type')
        scope = token_data.get('scope',"")

        if not access_token:
            raise ValidationError("failed_to_obtain_access_token")
        
        #step 2: Fetch GitHub User
        github_user = GitHubOAuthClient.get_github_user(access_token)
        github_user_id = github_user.get('id')
        if not github_user_id:
            raise ValidationError("failed_to_fetch_github_user")
        username = github_user.get('login')
        #step 3: Prevent linking same GitHub account to different users

        if GitHubAccount.objects.filter(
            github_user_id = github_user_id
        ).exclude(user=user).exists():
            raise ValidationError("This GitHub account is already linked to another user.")
        
        #Step 4: Calculate token expiry time 
        expires_at = None
        if expires_in:
            expires_at = timezone.now() + timedelta(seconds=expires_in)
        
        #step 5: Save or update Records
        GitHubAccount.objects.update_or_create(
            user = user,
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

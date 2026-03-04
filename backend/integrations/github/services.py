from django.db import transaction
from django.core.exceptions import ValidationError

from .models import GitHubAccount
from .client import GitHubOAuthClient

class GitHubService:
    @staticmethod
    @transaction.atomic
    def connect_github(user,code):
        pass

    
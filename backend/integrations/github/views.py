import secrets
from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class GitHubAuthorizationView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        state = secrets.token_urlsafe(16)

        request.session["github_oauth_state"] = state

        params = {
            "client_id": settings.GITHUB_CLIENT_ID,
            "redirect_uri": settings.GITHUB_REDIRECT_URI,
            "scope": "repo user",
            "state": state,
        }

        authorization_url = (
            "https://github.com/login/oauth/authorize?"
            + urlencode(params)
        )

        return redirect(authorization_url)
import secrets
from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect
from httpx import request
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import User

from rest_framework import status
from django.core.exceptions import ValidationError
from .services import GitHubService
from rest_framework.permissions import AllowAny

from django.core.signing import dumps
from django.core.signing import loads
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import TokenError
from urllib.parse import urlencode
import secrets
import secrets
from django.conf import settings

class GitHubAuthorizationView(APIView):
    permission_classes = [AllowAny]  # Require login

    def get(self, request):
        # Store user ID and CSRF token in session
        request.session['github_user_id'] = request.user.id
        request.session['github_oauth_state'] = secrets.token_urlsafe(16)

        # Build GitHub OAuth URL
        params = {
            "client_id": settings.GITHUB_CLIENT_ID,
            "redirect_uri": settings.GITHUB_REDIRECT_URI,
            "scope": "repo user",
            "state": request.session['github_oauth_state']
        }
        from urllib.parse import urlencode
        github_url = "https://github.com/login/oauth/authorize?" + urlencode(params)
        return redirect(github_url)

class GitHubCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.query_params.get("code")
        state = request.query_params.get("state")

        # Validate presence
        if not code or not state:
            return redirect("http://localhost:5173/app?github_linked=0")

        # Validate state matches session
        session_state = request.session.get("github_oauth_state")
        if state != session_state:
            return redirect("http://localhost:5173/app?github_linked=0")

        # Get user ID from session
        user_id = request.session.get("github_user_id")
        if not user_id:
            return redirect("http://localhost:5173/app?github_linked=0")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect("http://localhost:5173/app?github_linked=0")

        try:
            GitHubService.connect_github(user=user, code=code)
        except ValidationError:
            return redirect("http://localhost:5173/app?github_linked=0")

        # Clear session after use
        request.session.pop("github_user_id", None)
        request.session.pop("github_oauth_state", None)

        # Success → redirect to frontend
        return redirect("http://localhost:5173/app?github_linked=1")
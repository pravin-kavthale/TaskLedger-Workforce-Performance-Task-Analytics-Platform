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


class GitHubAuthorizationView(APIView):
    permission_classes = [AllowAny]  # don't rely on DRF auth

    def get(self, request):
        # Get JWT from query param
        token = request.query_params.get("token")
        if not token:
            return Response({"detail": "Token required"}, status=401)

        try:
            # Decode JWT manually
            untoken = UntypedToken(token)
            payload = untoken.payload
            user_id = payload.get("user_id")
            user = User.objects.get(id=user_id)
        except (TokenError, User.DoesNotExist):
            return Response({"detail": "Invalid token"}, status=401)

        # Generate OAuth state with user_id
        state_data = dumps({
            "user_id": user.id,
            "csrf": secrets.token_urlsafe(16)
        })

        # Build GitHub OAuth URL
        params = {
            "client_id": settings.GITHUB_CLIENT_ID,
            "redirect_uri": settings.GITHUB_REDIRECT_URI,
            "scope": "repo user",
            "state": state_data,
        }

        authorization_url = "https://github.com/login/oauth/authorize?" + urlencode(params)
        return redirect(authorization_url)
 

class GitHubCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.query_params.get("code")
        state = request.query_params.get("state")

        if not code or not state:
            return redirect("http://localhost:3000/dashboard?github_linked=0")

        try:
            data = loads(state)
            user_id = data.get("user_id")
            user = User.objects.get(id=user_id)
        except Exception:
            return redirect("http://localhost:3000/dashboard?github_linked=0")

        try:
            GitHubService.connect_github(user=user, code=code)
        except ValidationError:
            return redirect("http://localhost:3000/dashboard?github_linked=0")

        # Success → redirect to frontend with query param
        return redirect("http://localhost:3000/dashboard?github_linked=1")
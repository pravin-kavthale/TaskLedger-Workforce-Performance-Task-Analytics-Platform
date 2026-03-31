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

class GitHubAuthorizationView(APIView):

    permission_classes = [IsAuthenticated] 

    def get(self, request):

        user = request.user

        state = dumps({
            "user_id": user.id
        })

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
    
 

class GitHubCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.query_params.get("code")
        state = request.query_params.get("state")

        if not code or not state:
            return Response(
                {"error": "Missing code or state"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            data = loads(state)
            user_id = data["user_id"]
        except Exception:
            return Response(
                {"error": "Invalid state"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.get(id=user_id)

        try:
            GitHubService.connect_github(user=user, code=code)
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "GitHub account linked successfully"},
            status=status.HTTP_200_OK
        )
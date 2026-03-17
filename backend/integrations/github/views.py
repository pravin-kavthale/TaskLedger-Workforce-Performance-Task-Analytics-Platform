import secrets
from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from django.core.exceptions import ValidationError
from .services import GitHubService

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

class GitHubCallbackView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        code =  request.query_parameters.get("code")
        state = request.query_parameters.get("state")

        stored_state = request.session.get("github_oauth_state")

        if not stored_state or state != stored_state:
            return Response({"error": "Invalid state parameter"}, status=status.HTTP_400_BAD_REQUEST)

        if not code:
            return Response({"error": "Missing code parameter"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            GitHubService.connect_github(user = request.user , code = code)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "GitHub account linked successfully"}, status=status.HTTP_200_OK)
        
        
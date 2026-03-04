from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .services import GitHubService


class GitHubCallbackView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pass
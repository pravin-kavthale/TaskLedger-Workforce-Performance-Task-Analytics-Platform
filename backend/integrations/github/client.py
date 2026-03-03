from datetime import timedelta
from django.utils import timezone

import requests
from django.conf import settings

class GitHubOAuthClient: 
    TOKEN_URL = "https://github.com/login/oauth/access_token" 
    USER_API_URL = "https://api.github.com/user"

    @staticmethod
    def exchange_code_for_token(code):
        response = requests.post(  #We are making an HTTP POST request to:https://github.com/login/oauth/access_token
            GitHubOAuthClient.TOKEN_URL, 
            headers={"Accept": "application/json"}, # By default, GitHub may return URL-encoded data. This header forces GitHub to return: Json 
            data={ #We send form data: This proves: "GitHub, I am the real backend app, and I am exchanging this code legitimately."
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
            },
            timeout = 10, #If GitHub takes more than 10 seconds, the request fails.
        )

        response.raise_for_status() #If GitHub returns:  400  401  500 etc, this will raise an exception immediately.his will raise an exception immediately.
        return response.json() # returns tokens
    
    @staticmethod
    def fetch_user(access_token):
        response = requests.get(
            GitHubOAuthClient.USER_API_URL, #This endpoint returns information about the authenticated GitHub user. Important detail: It does NOT take user ID as parameter. It determines the user based purely on the access token.
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github.v3+json",
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    
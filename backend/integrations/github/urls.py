from django.urls import path
from .views import GitHubAuthorizationView, GitHubCallbackView

urlpatterns = [
    path("connect/", GitHubAuthorizationView.as_view()),
    path("callback/", GitHubCallbackView.as_view()),
]
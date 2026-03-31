from django.contrib import admin
from django.urls import path, include
from integrations.github.views import GitHubAuthorizationView, GitHubCallbackView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),     
    path("api/organization/", include("organization.urls")),
    path("api/work/", include("work.urls")),
    path("api/integrations/github/", include("integrations.github.urls")),
]
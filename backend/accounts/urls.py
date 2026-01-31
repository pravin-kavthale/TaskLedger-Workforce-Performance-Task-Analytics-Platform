from django.contrib import admin
from django.urls import path


from .views import CreateUserView, CustomTokenObtainPairView,ProtectedTestView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/protected/', ProtectedTestView.as_view(), name='protected_test'),
    path('auth/create-user/', CreateUserView.as_view(), name='create_user'),
]

from django.contrib import admin
from django.urls import path


from .views import CreateUserView, CustomTokenObtainPairView, ProtectedTestView, CurrentUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', CurrentUserView.as_view(), name='current_user'),
    path('auth/protected/', ProtectedTestView.as_view(), name='protected_test'),


    
    path('users/', CreateUserView.as_view(), name='create_user'),
]

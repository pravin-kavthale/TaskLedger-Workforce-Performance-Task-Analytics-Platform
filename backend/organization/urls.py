from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet



# this will include 
# GET /departments/
# GET /departments/{id}/
# POST /departments/
# PATCH /departments/{id}/ (only for 'is_activate' field)
router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')

urlpatterns = [
    path('', include(router.urls)),
]


from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AssignmentViewSet, ProjectViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'assignments', AssignmentViewSet, basename='assignment')

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AssignmentViewSet, ProjectViewSet, UserProjectViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r"users/(?P<user_pk>\d+)/projects",UserProjectViewSet,basename="user-projects",)


urlpatterns = [
    path('', include(router.urls)),
]

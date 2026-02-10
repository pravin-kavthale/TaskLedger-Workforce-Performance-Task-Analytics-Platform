from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AssignmentViewSet, ManagerProjectViewSet, ProjectMemberViewSet, ProjectViewSet, TaskViewSet, UserProjectViewSet

router = DefaultRouter()

router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'projects/(?P<project_pk>\d+)/tasks',TaskViewSet,basename='project-tasks')
urlpatterns = [
    path('', include(router.urls)),

    path('users/<int:user_pk>/projects/',UserProjectViewSet.as_view({'get': 'list'}),name='user-projects'),
    path('projects/<int:project_pk>/members/',ProjectMemberViewSet.as_view({'get': 'list'}),name='project-members'),
    path('managers/<int:manager_pk>/projects/', ManagerProjectViewSet.as_view({'get': 'list'}), name='manager-projects'),
]

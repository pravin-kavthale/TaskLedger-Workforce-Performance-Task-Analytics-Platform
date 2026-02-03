from django.shortcuts import render
from rest_framework import viewsets, mixins
from . models import Department
from . serializers import DepartmentSerializer
from . permissions import IsAdminUser 
from rest_framework.exceptions import MethodNotAllowed
from rest_framework_simplejwt.authentication import JWTAuthentication

class DepartmentViewSet(
    mixins.ListModelMixin,    # GET /departments/
    mixins.RetrieveModelMixin,# GET /departments/{id}/
    mixins.CreateModelMixin,  # POST /departments/
    viewsets.GenericViewSet
):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def partial_update(self, request, *args, **kwargs):
        # Allow patch only for 'is_active' field
        instance = self.get_object()
        if 'is_active' not in request.data:
            raise MethodNotAllowed(request.method, detail="Only 'is_active' can be updated.")
        return super().partial_update(request, *args, **kwargs)
    
    # Disable PUT and DELETE methods
    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method, detail="Full update is not allowed. Use PATCH to update 'is_active' only.")
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method, detail="Delete operation is not allowed.")
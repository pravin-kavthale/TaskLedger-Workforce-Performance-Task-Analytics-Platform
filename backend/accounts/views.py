from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, UserReadSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.permissions import UserPermission
from .serializers import CreateUserSerializer, CurrentUserSerializer, UpdateUserSerializer, UserReadSerializer
from .models import User 

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ProtectedTestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        return Response({
            "message": "You are authenticated",
            "user_id": request.user.id,
            "username": request.user.username,
            "role": request.user.role
        })


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CurrentUserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

class CreateUserView(APIView):
    permission_classes = [UserPermission]
    
    def get(self, request):
        users = User.objects.all()

        # Managers can only see employees
        if request.user.role == User.Role.MANAGER:
            users = users.filter(role=User.Role.EMPLOYEE)

        serializer = UserReadSerializer(users, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = CreateUserSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "message": "User created successfully",
            "user_id": user.id,
            "role": user.role,
            "created_by": user.created_by.id if user.created_by else None
        },status=201)

class UserDetailView(APIView):
    permission_classes = [UserPermission]

    def get_object(self, pk):
        try:
            obj = User.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"error": "User not found"}, status=404)

        serializer = UserReadSerializer(user)   
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"error": "User not found"}, status=404)

        serializer = UpdateUserSerializer(
            user,
            data=request.data,
            context={"request": request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
            },
            status=200
        )

    def delete(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"error": "User not found"}, status=404)

        if request.user.id == user.id:
            return Response(
                {"error": "You cannot deactivate yourself"},
                status=400
            )

        user.is_active = False
        user.save(update_fields=["is_active"])

        return Response(
            {"message": "User deactivated successfully"},
            status=200
        )

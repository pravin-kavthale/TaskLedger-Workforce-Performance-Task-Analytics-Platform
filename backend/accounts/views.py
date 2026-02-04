from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView # type: ignore
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore

from .permissions import IsAdmin, IsAdminOrManager
from .serializers import CreateUserSerializer, CurrentUserSerializer, UpdateUserSerializer
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
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    def get(self, request):
        users = User.objects.all()

        # Managers can only see EMPLOYEEs
        if request.user.role == User.Role.MANAGER or request.user.role == User.Role.MANAGER:
            users = users.filter(role=User.Role.EMPLOYEE)

        serializer = CurrentUserSerializer(
            users,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)
    
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
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        # Managers can only modify EMPLOYEEs
        if (
            request.user.role == User.Role.MANAGER
            and user.role != User.Role.EMPLOYEE
        ):
            return Response(
                {"error": "Managers can only manage employees"},
                status=403
            )

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
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        # Prevent self-delete
        if request.user.id == user.id:
            return Response(
                {"error": "You cannot delete yourself"},
                status=400
            )

        # Managers cannot delete admins or other managers
        if (
            request.user.role == User.Role.MANAGER
            and user.role != User.Role.EMPLOYEE
        ):
            return Response(
                {"error": "Managers can only delete employees"},
                status=403
            )

        user.delete()
        return Response(status=204)
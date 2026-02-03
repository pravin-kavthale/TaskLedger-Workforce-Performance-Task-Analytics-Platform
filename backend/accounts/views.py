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
        })

class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    def put(self, request, user_id):
         
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        serializer = UpdateUserSerializer(
            user,
            data=request.data,
            context={"request": request},
            partial=True # Allows PATCH-like behavior
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Return minimal user info after update
        return Response({
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active
        }, status=200)


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        # Optional safety: prevent admin from deleting themselves
        if request.user.id == user.id:
            return Response({"error": "You cannot delete yourself"}, status=400)

        user.delete()
        # Return 204 No Content as per REST convention
        return Response(status=204)
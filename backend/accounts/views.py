from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView # type: ignore
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore

from .permissions import IsAdmin, IsAdminOrManager
from .serializers import CreateUserSerializer

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
            "role": user.role
        })

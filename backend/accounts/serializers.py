from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['role'] = user.role
        token['user_id'] = user.id
        token['username'] = user.username
        token['email'] = user.email

        return token

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','role','password']
        extra_kwargs = {"password": {"write_only": True}}

        def vaidate_role(self,value):
            request_user = self.context['request'].user
            if request_user.role == 'admin':
                return value
            if request_user.role == 'manager' and value == 'employee':
                return value
            
            raise serializers.ValidationError("You cannot assign this role")
            
        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user
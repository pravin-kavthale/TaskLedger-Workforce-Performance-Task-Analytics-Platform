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

class CurrentUserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role', 'avatar_url']

    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','role','password']
        extra_kwargs = {"password": {"write_only": True}}

        def vaidate_role(self,value):
            request_user = self.context['request'].user
            if request_user.role == User.Role.ADMIN:
                return value

            if request_user.role == User.Role.MANAGER and value == User.Role.EMPLOYEE:
                return value

            
            raise serializers.ValidationError("You cannot assign this role")
            
        def create(self, validated_data):
            user = User.objects.create_user(**validated_data,created_by=self.context['request'].user)
            return user
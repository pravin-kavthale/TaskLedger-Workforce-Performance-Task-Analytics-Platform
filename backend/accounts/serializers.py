from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User
from .services import can_assign_role

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

class BaseUserRoleValidationMixin:
    def validate_role(self, value):
        request_user = self.context['request'].user
        if not can_assign_role(request_user, value):
            raise serializers.ValidationError("You cannot assign this role")
        return value

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

class CreateUserSerializer(BaseUserRoleValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(
            **validated_data,
            created_by=self.context['request'].user
        )
    

class UpdateUserSerializer(BaseUserRoleValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'is_active', 'avatar']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = []
    def delete(self, instance):
        instance.delete()
        
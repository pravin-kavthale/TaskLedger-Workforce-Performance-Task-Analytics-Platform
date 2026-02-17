from urllib import request
from requests import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from work.helper import is_admin
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
        fields = ['id', 'email', 'username', 'role', 'avatar_url','department','team']

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
        fields = ['id', 'username', 'email', 'role', 'password','department','team']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(
            **validated_data,
            created_by=self.context['request'].user
        )
    

class UpdateUserSerializer(BaseUserRoleValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'is_active', 'avatar','department','team']

    def update(self, instance, validated_data):
        request = self.context.get("request")
        current_user = request.user if request else None

        new_team = validated_data.get("team")

        if new_team is not None:
            # Case 1: user has no team yet → allow admin or manager of target team
            if instance.team is None:
                if not is_admin(current_user) and new_team.manager != current_user:
                    raise serializers.ValidationError(
                        "Only admin or manager of the target team can assign this user."
                    )
            # Case 2: user already has a team → cant change team directly, must contact admin
            else:
                if not is_admin(current_user):
                    raise serializers.ValidationError(
                        "user already has a team, cannot change team directly. Please contact admin."
                    )

        # Apply all validated fields
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
        
class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_active','department','team']
        
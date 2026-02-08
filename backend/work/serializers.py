from rest_framework import serializers


from .models import Project 
from rest_framework import serializers
from .models import Project, Assignment


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'code',
            'description', 
            'department',
            'manager',
            'status',
            'start_date',
            'end_date',
            'created_by',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'created_by',
            'created_at',
            'updated_at',
        ]

            
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        project = Project.objects.create(**validated_data)
        return project

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = [
            'id',
            'project',
            'user',
            'role',
            'assigned_at',
            'assigned_by',
            'is_active',
        ]
        read_only_fields =[
            'id',
            'assigned_at',
        ]
    
class UserProjectSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(source='project.id', read_only = True)
    project_name = serializers.CharField(source='project.name', read_only = True)
    project_code = serializers.CharField(source='project.code', read_only = True)
    assigned_by = serializers.CharField(
        source="assigned_by.username", read_only=True
    )
    class Meta:
        model = Assignment
        fields = [
            "user_id",
            "username",
            "email",
            "role",
            "assigned_at",
            "assigned_by",
        ]

class ProjectMemberSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source = 'user.id' , read_only = True)
    username = serializers.CharField(source = 'user.username', read_only = True)
    email = serializers.EmailField(source = 'user.email', read_only = True)
    role = serializers.CharField()
    class Meta:
        model = Assignment
        fields = [
            'user_id','username','email','role','assigned_at','assigned_by','is_active'
        ]
        read_only_fields = [
            'assigned_at',
        ]
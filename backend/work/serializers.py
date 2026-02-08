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
            'unassigned_at',
            'assigned_by',
            'is_active',
        ]
        read_only_fields =[
            'id',
            'assigned_at',
        ]
    
class UserProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields=[
            'project','role','assigned_at','unassigned_at','assigned_by','is_active'
        ]
        read_only_fields = [
            'assigned_at',
        ]
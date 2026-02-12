from rest_framework import serializers

from accounts.models import User
from .models import Project 
from rest_framework import serializers
from .models import Project, Assignment, Task
from django.core.exceptions import ValidationError,PermissionDenied

from .helper import is_admin, is_project_employee, is_project_manager, is_team_member

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'code',
            'description', 
            'department',
            'team',
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
            'manager'
        ]
    
    def validate(self,attrs):
        request = self.context['request']
        team = attrs.get('team')
        user = request.user

        if not team:
            raise serializers.ValidationError("Team is required.")
        # Rule 1: Only ADMIN or team manager can create project
        if user.role != "ADMIN" and team.manager != user:
            raise PermissionDenied(
                "Only ADMIN or the Team Manager can create a project."
            )
        
        department = attrs.get("department")
        if department and team.department != department:
            raise serializers.ValidationError(
                "Project department must match team department."
            )
        return attrs

            
    def create(self, validated_data):
        request = self.context["request"]
        validated_data["created_by"] = request.user
        return super().create(validated_data)

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
            'assigned_by',
        ]
    
    def validate(self,attrs):
        request = self.context['request']
        user = request.user
        project  = attrs.get('project')
        assigne = attrs.get('user')
        
        if user != project.manager and user.role != User.Role.ADMIN:
            raise PermissionDenied(
                "Only the project manager or ADMIN can assign users to this project."
            )
        
        if assigne and not is_team_member(assigne, team=project.team):
            raise serializers.ValidationError(
                "Assignee must be a member of the project team."
            )
        return attrs
    
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["assigned_by"] = request.user
        return super().create(validated_data)

    

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
            "project_id",
            "project_name",
            "project_code",
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

class TaskReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = [
            'id',
            'project',
            'created_by',
            'created_at',
        ]

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'priority',
            'estimated_hours',
            'status',
            'assigned_to',
        ]
        read_only_fields = [
            'id',
        ]

    def validate_assigned_to(self, user):
        request = self.context["request"]
        project_id = request.parser_context["kwargs"]["project_pk"]

        if not Assignment.objects.filter(
            project_id=project_id,
            user=user,
            is_active=True
        ).exists():
            raise serializers.ValidationError(
                "Assignee must belong to this project."
            )
        return user
        
        
class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "priority",
            "estimated_hours",
            "status",
            "assigned_to",
        ]

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user
        task = self.instance
        project = task.project

        # ADMIN → unrestricted
        if is_admin(user):
            return attrs

        # EMPLOYEE rules
        if user.role == User.Role.EMPLOYEE:
            illegal_fields = set(attrs.keys()) - {"status"}
            if illegal_fields:
                raise serializers.ValidationError(
                    "Employees can only update task status."
                )

            new_status = attrs.get("status")

            if task.status == Task.Status.DONE:
                raise serializers.ValidationError(
                    "Completed tasks are immutable."
                )

            if (
                task.status == Task.Status.BLOCKED
                and new_status
                and new_status != Task.Status.BLOCKED
            ):
                raise serializers.ValidationError(
                    "Only managers can unblock tasks."
                )

            return attrs

        # MANAGER rules
        if is_project_manager(user, project):
            new_status = attrs.get("status")

            if task.status == Task.Status.DONE:
                raise serializers.ValidationError(
                    "Completed tasks are immutable."
                )

            return attrs

        # Anything else is forbidden
        raise PermissionDenied("You do not have permission to update this task.")

    def validate_assigned_to(self, new_user):
        request = self.context["request"]
        user = request.user
        task = self.instance
        project = task.project

        # ADMIN → unrestricted
        if is_admin(user):
            return new_user

        # MANAGER only, and only within project
        if not is_project_manager(user, project):
            raise serializers.ValidationError(
                "Only the project manager can reassign tasks."
            )

        if not is_project_employee(new_user, project):
            raise serializers.ValidationError(
                "Assignee must belong to the same project."
            )

        return new_user

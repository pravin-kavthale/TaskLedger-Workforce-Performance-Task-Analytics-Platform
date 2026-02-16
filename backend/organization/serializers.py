from rest_framework import serializers

from accounts.models import User
from .models import Department, Team

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields=['id','name','code','is_active','created_at','updated_at','created_by']
        read_only_fields=['created_at','updated_at','created_by']

    def validate(self,attrs):
        request_user = self.context['request'].user
        if request_user.role != "ADMIN":
            raise serializers.ValidationError("Only Admin users can create a department.")
        return attrs
        
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        department = Department.objects.create(**validated_data)
        return department
        
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'code',
            'department',
            'manager',
            'is_activate',
        ]
    
    def validate_manager(self, manager):
        if manager.role != User.Role.MANAGER:
            raise serializers.ValidationError(
                "Selected user must have MANAGER role."
            )
        return manager
    
    def validate(self, attrs):
        department = attrs.get("department", getattr(self.instance, "department", None))
        manager = attrs.get("manager", getattr(self.instance, "manager", None))

        if manager and department and manager.department != department:
            raise serializers.ValidationError(
                "Manager's department must match the team's department."
            )
        return attrs
    
    def create(self,validated_data):
        team = super().create(validated_data)

        manager = team.manager
        if manager:
            manager.team = team
            manager.save(update_fields = ['team'])
        
        return team
    
    def update(self,instance,validated_data):
            old_manager = instance.manager
            team = super().update(instance, validated_data)
            new_manager = team.manager

            if old_manager != new_manager:
                if old_manager:
                    old_manager.team = None
                    old_manager.save(update_fields=['team'])
                
                if new_manager:
                    new_manager.team = team
                    new_manager.save(update_fields=['team'])
            return team 
    

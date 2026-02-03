from rest_framework import serializers
from .models import Department

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
        
from .models import Task, CustomUser
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
class TaskSerializer(serializers.ModelSerializer):
    assigned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to', 'assigned_by', 'status', 'created_at']
        read_only_fields = ['assigned_by', 'created_at']

    def validate(self, data):
        request_user = self.context['request'].user
        
        # Ensure only Team Leads can assign tasks
        if request_user.role != 'team_lead':
            raise serializers.ValidationError("Only Team Leads can assign tasks.")
        
        return data

    def create(self, validated_data):
        validated_data['assigned_by'] = self.context['request'].user
        return super().create(validated_data)
from rest_framework import serializers
from role.models import Role

class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = [
            'id', 'title', 'description', 'is_active', 'created_at','created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = ['created_at']
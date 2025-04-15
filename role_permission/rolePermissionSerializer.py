from rest_framework import serializers
from role_permission.models import RolePermission

from role.roleSerializer import RoleSerializer

class RolePermissionSerializer(serializers.ModelSerializer):

    role_id = serializers.CharField()

    role_data = RoleSerializer(source='role', read_only=True)

    class Meta:
        model = RolePermission
        fields = [
            'id', 'role_id','role_data', 'model', 'action',
            'is_active', 'created_at','created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = ['created_at']
# from rest_framework import serializers
# from user.models import User

# from role.roleSerializer import RoleSerializer

# class UserStoreSerializer(serializers.ModelSerializer):

#     role_id = serializers.CharField()

#     role_data = RoleSerializer(source='role', read_only=True)

#     class Meta:
#         model = User
#         fields = [
#             'id', 'role_id','role_data', 'model', 'action',
#             'is_active', 'created_at','created_by', 'updated_at', 'updated_by'
#         ]
#         read_only_fields = ['created_at']


from rest_framework import serializers
from user.models import User

from role.roleSerializer import RoleSerializer

class UserSerializer(serializers.ModelSerializer):

    role_id = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    role_data = RoleSerializer(source='role', read_only=True)

    class Meta:
        model = User
        # fields = [
        #     'id', 'email', 'name', 'role_id','role_data',
        #     'is_active', 'is_staff',
        #     'created_at', 'created_by', 'updated_at', 'updated_by'
        # ]
        # In UserSerializer

        fields = [
        'id', 'email', 'name', 'password', 'role_id', 'role_data',
        'is_active', 'is_staff',
        'created_at', 'created_by', 'updated_at', 'updated_by'
        ]

        read_only_fields = ['id', 'is_active', 'is_staff', 'created_at', 'updated_at', 'created_by', 'updated_by']

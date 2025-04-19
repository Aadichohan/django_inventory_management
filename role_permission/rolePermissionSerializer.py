# from rest_framework import serializers
# from role_permission.models import RolePermission

# from role.roleSerializer import RoleSerializer
# from endpoint_master.models import EndpointMaster

# class RolePermissionSerializer(serializers.ModelSerializer):

#     role_id = serializers.CharField()
#     end_id = serializers.CharField()

#     role_data = RoleSerializer(source='role', read_only=True)

#     class Meta:
#         model = RolePermission
#         fields = [
#             'id', 'role_id','role_data', 'model', 'action',
#             'is_active', 'created_at','created_by', 'updated_at', 'updated_by'
#         ]
#         read_only_fields = ['created_at', 'created_by', 'role_data']

from rest_framework import serializers
from role_permission.models import RolePermission
from endpoint_master.models import EndpointMaster
from role.roleSerializer import RoleSerializer
from endpoint_master.endpoint_master_serializer import EndpointMasterSerializer

class RolePermissionSerializer(serializers.ModelSerializer):
    role_id = serializers.CharField()
    endpoint_id = serializers.CharField(required=False, allow_blank=True)
    endpoint_title = serializers.CharField(required=False, write_only=True)

    role_data = RoleSerializer(source='role', read_only=True)
    endpoint_data = EndpointMasterSerializer(source='endpoint', read_only=True)

    class Meta:
        model = RolePermission
        fields = [
            'id', 'role_id', 'role_data', 'allowed_methods',
            'is_active', 'created_at', 'created_by',
            'updated_at', 'updated_by',
            'endpoint_id', 'endpoint_title', 'endpoint_data'
        ]
        read_only_fields = ['created_at', 'created_by', 'role_data', 'endpoint_data']

    def validate(self, attrs):
        # Check if endpoint_id is missing and endpoint_title is present
        endpoint_id = attrs.get('endpoint_id')
        endpoint_title = attrs.get('endpoint_title')

        if not endpoint_id:
            if endpoint_title:
                try:
                    endpoint_master = EndpointMaster.objects.get(title=endpoint_title)  # use correct field here
                    attrs['endpoint_id'] = str(endpoint_master.id)
                except EndpointMaster.DoesNotExist:
                    raise serializers.ValidationError("Endpoint with this title does not exist.")
            else:
                raise serializers.ValidationError("Either 'endpoint_id' or 'endpoint_title' must be provided.")

        # 🧽 Remove endpoint_title so it's not passed to model creation
        attrs.pop('endpoint_title', None)

        return attrs

    # def validate(self, attrs):
    #     # Check if endpoint_id is missing and endpoint_title is present
    #     endpoint_id = attrs.get('endpoint_id')
    #     endpoint_title = attrs.get('endpoint_title')

    #     if not endpoint_id:
    #         if endpoint_title:
    #             try:
    #                 endpoint_master = EndpointMaster.objects.get(title=endpoint_title)
    #                 print('endpoint_master ',endpoint_master)
    #                 attrs['endpoint_id'] = str(endpoint_master.id)
    #             except EndpointMaster.DoesNotExist:
    #                 raise serializers.ValidationError("Endpoint with this title does not exist.")
    #         else:
    #             raise serializers.ValidationError("Either 'endpoint_id' or 'endpoint_title' must be provided.")

    #     return attrs

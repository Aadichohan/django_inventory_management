from rest_framework import serializers
from endpoint_master.models import EndpointMaster


class EndpointMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndpointMaster
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']
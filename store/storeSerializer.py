from rest_framework import serializers
from store.models import Store

class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = [
            'id', 'title', 'loaction', 'description', 'is_active', 'created_at','created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = ['created_at', 'created_by']
from rest_framework import serializers
from customer.models import Customer

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'contact_no','address', 'is_active', 'created_at','created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = ['created_at']
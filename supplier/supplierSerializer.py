from rest_framework import serializers
from supplier.models import Supplier

class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'contact_no','address', 'is_active', 'created_at','created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = ['created_at', 'created_by']
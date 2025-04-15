from rest_framework import serializers
from product.models import Product

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'is_active', 'created_at','created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = ['created_at']

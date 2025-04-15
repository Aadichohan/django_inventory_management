from rest_framework import serializers
from product.models import Product
from category.categorySerializer import CategorySerializer
class ProductSerializer(serializers.ModelSerializer):
    category_id  = serializers.CharField()

    category_data = CategorySerializer(source='category', read_only=True)
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'sku','price','description', 'category_id', 'category_data','is_active', 'created_at','created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = ['created_at', 'created_by']

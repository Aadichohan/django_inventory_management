from rest_framework import serializers
from store_product.models import StoreProduct

from product.productSerializer import ProductSerializer
from store.storeSerializer import StoreSerializer

class StoreProductSerializer(serializers.ModelSerializer):

    product_id = serializers.CharField()
    store_id = serializers.CharField()

    # ✅ READ using nested object
    product_data = ProductSerializer(source='product', read_only=True)
    store_data    = StoreSerializer(source='store', read_only=True)
    class Meta:
        model = StoreProduct
        fields = [
            'id', 'product_id','product_data', 'store_id' 'store_data', 'quantity', 'custom_price', 'description'
            'is_active', 'created_at','created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = ['created_at', 'created_by']
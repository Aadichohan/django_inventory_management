from rest_framework import serializers
from sales_order.models import SalesOrder

from product.productSerializer import ProductSerializer
from customer.customerSerializer import CustomerSerializer

class StoreProductSerializer(serializers.ModelSerializer):

    customer_id = serializers.CharField()
    product_id  = serializers.CharField()

    # ✅ READ using nested object
    customer_data = CustomerSerializer(source='customer', read_only=True)
    product_data  = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = SalesOrder
        fields = [
            'id', 'customer_id','customer_data','product_id','product_data', 'quantity', 'total_price',
            'is_active', 'created_at','created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = ['created_at']
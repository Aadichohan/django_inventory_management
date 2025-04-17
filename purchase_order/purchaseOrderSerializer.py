from rest_framework import serializers
from purchase_order.models import PurchaseOrder

from product.productSerializer import ProductSerializer
from supplier.supplierSerializer import SupplierSerializer

class PurchaseOrderSerializer(serializers.ModelSerializer):

    supplier_id = serializers.CharField()
    product_id  = serializers.CharField()

    supplier_data = SupplierSerializer(source='supplier', read_only=True)
    product_data = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'supplier_id','supplier_data','product_id','product_data', 'quantity', 'total_price',
            'is_active', 'created_at','created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = ['created_at', 'created_by']
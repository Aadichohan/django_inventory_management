from rest_framework import serializers
from purchase_order.models import PurchaseOrder

from supplier.supplierSerializer import SupplierSerializer
from product.productSerializer import ProductSerializer
from store.storeSerializer import StoreSerializer

class PurchaseOrderSerializer(serializers.ModelSerializer):

    supplier_id = serializers.CharField()
    product_id  = serializers.CharField()
    store_id  = serializers.CharField()

    total_price_data = serializers.SerializerMethodField()

    supplier_data = SupplierSerializer(source='supplier', read_only=True)
    product_data = ProductSerializer(source='product', read_only=True)
    store_data = StoreSerializer(source='store', read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'supplier_id','supplier_data','product_id','product_data', 'store_id', 'store_data','quantity', 'total_price', 'total_price_data', 'unit_price',
            'is_active', 'created_at','created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = ['created_at', 'created_by']

    def get_total_price_data(self, obj):
        request = self.context.get('request', None)
        # method = request.method
        if request and request.method in ['GET']:
            quantity = obj.quantity
            unit_price = obj.unit_price
        elif request.method in ['POST', 'PUT', 'PATCH']:
            quantity = obj.quantity
            unit_price = obj.unit_price
        if quantity is not None and unit_price is not None:
            return quantity * unit_price
        return None

    # def validate(self, attrs):
    #     # calculate and inject total_price before saving
    #     quantity = attrs.get('quantity')
    #     unit_price = attrs.get('unit_price')

    #     if quantity is not None and unit_price is not None:
    #         attrs['total_price'] = quantity * unit_price

        # return attrs
    def validate_unit_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Unit price cannot be negative.")
        return value

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value
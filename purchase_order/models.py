from django.db import models
from django.contrib.auth.models import User
from supplier.models import Supplier
from product.models import Product

class PurchaseOrder(models.Model):
    id = models.AutoField(primary_key=True)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='purchase_order')
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='purchase_order')
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active    = models.BooleanField(default=True) 
    created_at  = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='purchase_order_created')
    updated_at   = models.DateTimeField(null=True, blank=True)  # manually handled
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='purchase_order_updated')

    def __str__(self):
        return f'{self.name} - {self.contact_no}'

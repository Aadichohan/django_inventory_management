from django.db import models
from django.conf import settings
from supplier.models import Supplier
from product.models import Product
from store.models import Store

class PurchaseOrder(models.Model):
    id = models.AutoField(primary_key=True)
    
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='purchase_order_supplier')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='purchase_order_product')
    store   = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, related_name='purchase_order_store')

    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    is_active = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name='purchase_order_created')
    updated_at = models.DateTimeField(null=True, blank=True)  # manually handled
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='purchase_order_updated')

    def __str__(self):
        return f'supplier.name: {self.supplier.name} | supplier.contact_no: {self.supplier.contact_no} | product.title: {self.product.title} | store: {self.store.title if self.store else "N/A"}'

    class Meta:
        db_table = 'purchase_order'



# from django.db import models
# from django.contrib.auth.models import User
# from django.conf import settings

# from supplier.models import Supplier
# from product.models import Product

# class PurchaseOrder(models.Model):
#     id = models.AutoField(primary_key=True)
#     supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='purchase_order')
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='purchase_order')
#     quantity = models.IntegerField()
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     is_active    = models.BooleanField(default=True) 
#     created_at  = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name='purchase_order_created')
#     updated_at   = models.DateTimeField(null=True, blank=True)  # manually handled
#     updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='purchase_order_updated')

#     def __str__(self):
#         return f' supplier.name: {self.supplier.name} | supplier.contact_no: {self.supplier.contact_no} | product.title : {self.product.title}'
    
#     class Meta:
#         db_table = 'purchase_order' 

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from customer.models import Customer
from product.models import Product
from store.models import Store

class SalesOrder(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, related_name='sales_order_customer')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False,  related_name='sales_order_product')
    store   = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, related_name='sales_order_store')
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2,  default=0.00)
    is_active    = models.BooleanField(default=True) 
    created_at  = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name='sales_order_created')
    # updated_at   = models.DateTimeField(null=True, blank=True)  # manually handled
    updated_at   = models.DateTimeField(null=True, blank=True)  # manually handled
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='sales_order_updated')

    def __str__(self):
        return f'Customer name: {self.customer.name} - Contact no: {self.customer.contact_no}| Product: {self.product.title} - Store:{self.store.title}'
    
    class Meta:
        db_table = 'sales_order' 

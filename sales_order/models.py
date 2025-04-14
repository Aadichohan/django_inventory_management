from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from customer.models import Customer
from product.models import Product

class SalesOrder(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, related_name='sales_order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False,  related_name='sales_order')
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active    = models.BooleanField(default=True) 
    created_at  = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name='sales_order_created')
    updated_at   = models.DateTimeField(null=True, blank=True)  # manually handled
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='sales_order_updated')

    def __str__(self):
        return f'{self.name} - {self.contact_no}'
    
    class Meta:
        db_table = 'sales_order' 

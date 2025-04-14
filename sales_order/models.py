from django.db import models
from django.contrib.auth.models import User
from customer.models import Customer
from product.models import Product

class SalesOrder(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, related_name='sales_order')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=False,  related_name='sales_order')
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active    = models.BooleanField(default=True) 
    created_at  = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='sales_order_created')
    updated_at   = models.DateTimeField(null=True, blank=True)  # manually handled
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sales_order_updated')

    def __str__(self):
        return f'{self.name} - {self.contact_no}'

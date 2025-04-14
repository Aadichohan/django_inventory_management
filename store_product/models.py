from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from store.models import Store

class StoreProduct(models.Model):
    id           = models.AutoField(primary_key=True)
    product_id   = models.ForeignKey(
        Product, related_name='product_store_product',
        on_delete=models.CASCADE
    )
    store_id     = models.ForeignKey(
        Store, related_name='product_store_store',
        on_delete=models.CASCADE
    )
    quantity     = models.IntegerField()
    custom_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description  = models.TextField(max_length=500, null=True, blank=True)
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    created_by   = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, related_name='product_store_created'
    )
    # created_by   = models.ForeignKey(
    #     User, related_name='product_store_created',
    #     on_delete=models.SET_NULL, null=False
    # )
    updated_at   = models.DateTimeField(null=True, blank=True)  # manually handled
    updated_by   = models.ForeignKey(User, related_name='product_store_updated', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.product_id.name} - {self.store_id.name}'

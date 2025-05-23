from django.db import models
from django.conf import settings
from product.models import Product
from store.models import Store

class StoreProduct(models.Model):
    id            = models.AutoField(primary_key=True)
    
    product       = models.ForeignKey(
        Product, related_name='product_store_product',
        on_delete=models.CASCADE
    )
    store         = models.ForeignKey(
        Store, related_name='product_store_store',
        on_delete=models.CASCADE
    )
    quantity      = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sell_price     = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # custom_price   = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description    = models.TextField(max_length=500, null=True, blank=True)
    is_active      = models.BooleanField(default=True)

    created_at     = models.DateTimeField(auto_now_add=True)
    created_by     = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name='product_store_created'
    )
    updated_at     = models.DateTimeField(null=True, blank=True)
    updated_by     = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='product_store_updated', on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f'{self.product.title} - {self.store.title}'

    class Meta:
        db_table = 'store_product'



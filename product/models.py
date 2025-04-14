from django.db import models
from django.contrib.auth.models import User
from category.models import Category

class Product(models.Model):
    title       = models.CharField(max_length=255)
    sku         = models.CharField(max_length=100, unique=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=500, null=True, blank=True)
    category    = models.ForeignKey(
        Category, related_name='product_category',
        on_delete=models.CASCADE, null=False
    )
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    created_by  = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, related_name='product_created'
    )
    updated_at = models.DateTimeField(null=True, blank=True)  # manually handled
    updated_by = models.ForeignKey(User, related_name='product_updated', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.sku})"

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)  
    contact_no = models.CharField(max_length=13)  
    address = models.CharField(max_length=255)
    is_active    = models.BooleanField(default=True) 
    created_at  = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, null=False, related_name='customer_created')
    updated_at   = models.DateTimeField(null=True, blank=True)  # manually handled
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='customer_updated')

    def __str__(self):
        return f'{self.name} - {self.contact_no}'

    class Meta:
        db_table = 'customer' 
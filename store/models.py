from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Store(models.Model):
    id = models.AutoField(primary_key=True)
    title       = models.CharField(max_length=255)
    loaction    = models.CharField(max_length=255)
    description = models.TextField(max_length=500, null=True, blank=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    created_by  = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name='store_created'
    )
    updated_at = models.DateTimeField(null=True, blank=True)  # manually handled
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='store_updated', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} | ({self.location})"
    
    class Meta:
        db_table = 'store' 

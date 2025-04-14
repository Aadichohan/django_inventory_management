from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

class Role(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    is_active    = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name='role_created')
    updated_at   = models.DateTimeField(null=True, blank=True)  # manually handled
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='role_updated')

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'role' 

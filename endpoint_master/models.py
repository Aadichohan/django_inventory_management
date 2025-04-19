# models.py
from django.db import models
from django.conf import settings

class EndpointMaster(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    endpoint = models.CharField(max_length=200, unique=True)  # e.g., "/api/products/"
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='endpoint_master_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='endpoint_master_updated'
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.endpoint}"

    class Meta:
        db_table = 'endpoint_master'
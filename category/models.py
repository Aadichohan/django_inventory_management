from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    title       = models.CharField(max_length=255)
    description = models.TextField(max_length=500, null=True, blank=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    created_by  = models.ForeignKey(
        User,  on_delete=models.CASCADE, null=False, related_name='category_created'
    )
    updated_at  = models.DateTimeField(null=True, blank=True)  # manually handled
    updated_by  = models.ForeignKey(User, related_name='category_updated', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

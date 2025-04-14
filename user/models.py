from django.db import models
from django.contrib.auth.models import User
from role.models import Role

class CustomUser(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255) 
    last_name = models.CharField(max_length=255) 
    email   = models.EmailField(unique=True)
    password = models.CharField(max_length=255) 
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, related_name='user_role')
    is_active    = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user_created')
    updated_at   = models.DateTimeField(null=True, blank=True)  # manually handled
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_updated')

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'

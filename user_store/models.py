from django.db import models
from django.contrib.auth.models import User
from store.models import Store

class UserStore(models.Model):
    id           = models.AutoField(primary_key=True)
    user_id   = models.ForeignKey(
        User, related_name='user_store_user',
        on_delete=models.CASCADE
    )
    store_id     = models.ForeignKey(
        Store, related_name='user_store_store',
        on_delete=models.CASCADE
    )
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    created_by   = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, related_name='user_store_created'
    )
    updated_at   = models.DateTimeField(null=True, blank=True)  # manually handled
    updated_by   = models.ForeignKey(User, related_name='user_store_updated', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.user_id.first_name} - {self.store_id.title}'

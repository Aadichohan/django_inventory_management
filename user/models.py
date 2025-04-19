# from django.db import models
# from django.contrib.auth.models import User
# from role.models import Role

# class CustomUser(models.Model):
#     id = models.AutoField(primary_key=True)
#     first_name = models.CharField(max_length=255) 
#     last_name = models.CharField(max_length=255) 
#     email   = models.EmailField(unique=True)
#     password = models.CharField(max_length=255) 
#     role = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, related_name='user_role')
#     is_active    = models.BooleanField(default=True)
#     created_at  = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user_created')
#     updated_at   = models.DateTimeField(null=True, blank=True)  # manually handled
#     updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_updated')

#     def __str__(self):
#         return f'{self.first_name} - {self.last_name}'
    
#     class Meta:
#         db_table = 'user' 


# accounts/models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from role.models import Role
from django.conf import settings
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    # role_id = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('manager', 'Manager'), ('staff', 'Staff')])
    # role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_role', default=3)


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_users')
    # updated_at = models.DateTimeField(auto_now=True)
    # updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_users')
    
    updated_at  = models.DateTimeField(null=True, blank=True)  # manually handled
    updated_by  = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_users', on_delete=models.SET_NULL, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'auth_user'

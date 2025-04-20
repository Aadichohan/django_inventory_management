from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.conf import settings
from role.models import Role
from endpoint_master.models import EndpointMaster


class RolePermission(models.Model):
    HTTP_METHODS = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('PATCH', 'PATCH'),
        ('DELETE', 'DELETE'),
    ]

    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    # model = models.CharField(max_length=50, null=True, default=True)
    endpoint = models.ForeignKey(EndpointMaster, on_delete=models.CASCADE, related_name='endpoint_master_table')  # Correct field name here
    allowed_methods = models.JSONField(default=list)  # Example: ["GET", "POST"]
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='role_permissions_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='role_permissions_updated'
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'role_permission'
        # unique_together = ('role', 'endpoint')

    def __str__(self):
        return f"{self.role} - {self.endpoint.endpoint}"
    
    def clean(self):
        if self.role_id and self.endpoint_id:
            # Only check if both values are present
            existing = RolePermission.objects.filter(
                role=self.role,
                endpoint=self.endpoint,
            )
            if self.pk:
                # Exclude self on update
                existing = existing.exclude(pk=self.pk)
                # print('existing ', existing)
            if existing.exists():
                # pass
                raise ValidationError("This role-endpoint combination already exists.")

    def save(self, *args, **kwargs):
        self.clean()  # ensure clean is called on save too
        super().save(*args, **kwargs)


# class RolePermission(models.Model):
#     # ROLES = [
#     #     ('staff', 'Staff'),
#     #     ('manager', 'Manager'),
#     #     ('admin', 'Admin'),
#     # ]
    
#     ACTIONS = [
#         ('create', 'Create'),
#         ('view', 'View'),
#         ('update', 'Update'),
#         ('delete', 'Delete'),
#     ]
    
#     id = models.AutoField(primary_key=True)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, related_name='role') 
#     # role = models.CharField(max_length=20, choices=ROLES)  # Role (staff, manager, admin)
#     model = models.CharField(max_length=50)
#     action = models.CharField(max_length=20, choices=ACTIONS)  # Action (create, view, update, delete)
#     is_active    = models.BooleanField(default=True) 
#     created_at = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name='role_permissions_created') 
#     updated_at   = models.DateTimeField(null=True, blank=True)
#     updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='role_permissions_updated') 

#     def __str__(self):
#         return f"{self.role} - {self.model} - {self.action}"
    

#     class Meta:
#         db_table = 'role_permission' 

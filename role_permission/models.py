from django.db import models
from django.contrib.auth.models import User
from role.models import Role

class RolePermission(models.Model):
    # ROLES = [
    #     ('staff', 'Staff'),
    #     ('manager', 'Manager'),
    #     ('admin', 'Admin'),
    # ]
    
    ACTIONS = [
        ('create', 'Create'),
        ('view', 'View'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]
    
    id = models.AutoField(primary_key=True)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, related_name='role') 
    # role = models.CharField(max_length=20, choices=ROLES)  # Role (staff, manager, admin)
    model = models.CharField(max_length=50)  # Model (sales_order, purchase_order, etc.)
    action = models.CharField(max_length=20, choices=ACTIONS)  # Action (create, view, update, delete)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='role_permissions_created') 
    updated_at   = models.DateTimeField(null=True, blank=True)  # manually handled
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='role_permissions_updated') 

    def __str__(self):
        return f"{self.role} - {self.model} - {self.action}"

from rest_framework.permissions import BasePermission
from .models import RolePermission, EndpointMaster
from django.db.models import Q

class RoleBasedPermission(BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        user = request.user
        if not user or not hasattr(user, 'role'):
            return False

        # ✅ Admin bypass
        if getattr(user, 'role_id', None) == 1:
            return True

        role = user.role
        path = request.path
        method = request.method.upper()
        print('p ',path)
        try:
            endpoint = EndpointMaster.objects.get(endpoint=path, is_active=True)
        except EndpointMaster.DoesNotExist:
            return False

        # permission = RolePermission.objects.filter(
        #     role=role,
        #     endpoint=endpoint,
        #     # allowed_methods__contains=[method],
        #     is_active=True
        # ).exists()

        permissions = RolePermission.objects.filter(
            role=role,
            endpoint=endpoint,
            is_active=True
        )

        permission = any(method in perm.allowed_methods for perm in permissions)
        # print('permission', permission)
        return permission
        # return RolePermission.objects.filter(
        #     role=role,
        #     endpoint_master=endpoint,
        #     allowed_methods__contains=[method],
        #     is_active=True
        # ).exists()

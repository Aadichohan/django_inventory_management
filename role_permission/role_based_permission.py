from rest_framework.permissions import BasePermission
from .models import RolePermission

class RoleBasedPermission(BasePermission):
    message = "You do not have role-based permission to perform this action."

    def has_permission(self, request, view):
        user = request.user
        print('userpermission: ', user)

        if not user or not hasattr(user, 'role'):
            return False

        # ✅ Admin full access
        if getattr(user, 'role_id', None) == 1:
            return True

        role = user.role
        model_name = getattr(view.queryset.model, '__name__', '').lower()

        method_action_map = {
            'GET': 'view',
            'POST': 'create',
            'PUT': 'update',
            'PATCH': 'update',
            'DELETE': 'delete',
        }

        action = method_action_map.get(request.method)
        if not action:
            return False

        return RolePermission.objects.filter(
            role=role,
            model=model_name,
            action=action
        ).exists()

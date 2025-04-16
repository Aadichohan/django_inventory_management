# # permissions.py

# from rest_framework.permissions import BasePermission
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# from role_permission.models import RolePermission

# def get_user_from_token(request):
#     header = request.headers.get('Authorization')
#     if not header or not header.startswith('Bearer '):
#         return None

#     try:
#         token = header.split(' ')[1]
#         validated_token = JWTAuthentication().get_validated_token(token)
#         user = JWTAuthentication().get_user(validated_token)
#         return user
#     except (IndexError, TokenError, InvalidToken):
#         return None

# class RoleBasedPermission(BasePermission):
#     message = "You do not have role-based permission to perform this action."

#     def has_permission(self, request, view):
#         # 🔒 Get user from token
#         user = get_user_from_token(request)
#         if user is None:
#             return False

#         role = getattr(user, 'role', None)
#         if not role:
#             return False

#         model_name = getattr(view.queryset.model, '__name__', '').lower()

#         method_action_map = {
#             'GET': 'view',
#             'POST': 'create',
#             'PUT': 'update',
#             'PATCH': 'update',
#             'DELETE': 'delete',
#         }

#         action = method_action_map.get(request.method)
#         if not action:
#             return False

#         # Check if role has permission for this model + action
#         return RolePermission.objects.filter(
#             role=role,
#             model=model_name,
#             action=action
#         ).exists()

from rest_framework.permissions import BasePermission
from .models import RolePermission
from rest_framework_simplejwt.authentication import JWTAuthentication

def get_user_from_token(request):
    header = request.headers.get('Authorization')
    if not header or not header.startswith('Bearer '):
        return None

    try:
        token = header.split(' ')[1]
        validated_token = JWTAuthentication().get_validated_token(token)
        user = JWTAuthentication().get_user(validated_token)
        return user
    except Exception:
        return None

class RoleBasedPermission(BasePermission):
    message = "You do not have role-based permission to perform this action."

    def has_permission(self, request, view):
        # ✅ Step 1: Get user from JWT token
        user = get_user_from_token(request)
        if not user:
            return False
        # print('as ',getattr(user, 'role_id', None))
        # print('Role Title:', getattr(user.role, 'title', None))
        # return False
        # ✅ Step 2: Bypass check if user is admin
        if getattr(user, 'role_id', None) == 1:
            return True  # Full access


        # ✅ Step 3: Role-based check for others
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


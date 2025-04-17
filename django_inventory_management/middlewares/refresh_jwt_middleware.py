from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from rest_framework import status
from django.utils.functional import SimpleLazyObject

import jwt
from django.conf import settings
from user.models import User


class RefreshJWTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.headers.get('Authorization')
        refresh_token = request.headers.get('X-Refresh-Token')  # custom header
        if auth_header and auth_header.startswith('Bearer '):
            access_token = auth_header.split(' ')[1]
            try:
                validated_token = AccessToken(access_token)
                user = JWTAuthentication().get_user(validated_token)
                print('token user: ', validated_token)
                print('token user: ', user)
                request.user = user
            except TokenError as e:
                print('TokenError ', e)
                # Access Token expired, try refresh
                if refresh_token:
                    try:
                        # token = RefreshToken(refresh_token)
                        # user = User.objects.get(id=token.payload['user_id'])
                        # new_access_token = str(token.access_token)
                        new_token = RefreshToken(refresh_token).access_token
                        request.new_access_token = str(new_token)
                        print('refresh_token ', refresh_token)
                        print('auth_header ', new_token)

                        # ⛔ IMPORTANT: Set the new token to request.META so DRF picks it up
                        request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_token}'
                        # request.user = user
                        # new_token = token.access_token
                         # ⛔ IMPORTANT: Set the new token to request.META so DRF picks it up
                        request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_token}'

                        # ✅ Re-authenticate the user manually
                        user_authenticator = JWTAuthentication()
                        user, validated_token = user_authenticator.authenticate(request)
                        request.new_access_token = validated_token
                        print('userToeknpermission: ',validated_token)
                        request.user = user
                    except Exception as e:
                        return JsonResponse(
                            {"error": "Invalid refresh token", "details": str(e)},
                            status=status.HTTP_401_UNAUTHORIZED
                        )
                else:
                    return JsonResponse(
                        {"error": "Access token expired. Refresh token required."},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

    def process_response(self, request, response):
        # If new access token was generated, attach it to the response
        if hasattr(request, 'new_access_token'):
            response['X-New-Access-Token'] = request.new_access_token
            print(response,' :req')
        return response

# from django.utils.deprecation import MiddlewareMixin
# from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# class RefreshTokenMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         auth = request.headers.get("Authorization", None)

#         if auth and auth.startswith("Bearer "):
#             token = auth.split(" ")[1]

#             try:
#                 # Try verifying access token
#                 AccessToken(token)
#             except TokenError:
#                 # Token is invalid or expired, try refreshing it
#                 refresh_token = request.headers.get("X-Refresh-Token", None)

#                 if refresh_token:
#                     try:
#                         new_token = RefreshToken(refresh_token).access_token
#                         request.new_access_token = str(new_token)

#                         # ⛔ IMPORTANT: Set the new token to request.META so DRF picks it up
#                         request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_token}'

#                         # ✅ Re-authenticate the user manually
#                         user_authenticator = JWTAuthentication()
#                         user, validated_token = user_authenticator.authenticate(request)
#                         request.user = user

#                     except TokenError:
#                         pass  # Invalid refresh token, 401 will be returned

#     def process_response(self, request, response):
#         if hasattr(request, 'new_access_token'):
#             response['X-New-Access-Token'] = request.new_access_token
#         return response

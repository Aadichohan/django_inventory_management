from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from rest_framework import status

class RefreshJWTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.headers.get('Authorization')
        refresh_token = request.headers.get('X-Refresh-Token')

        if auth_header and auth_header.startswith('Bearer '):
            access_token = auth_header.split(' ')[1]
            user_authenticator = JWTAuthentication()

            # Step 1: Manually validate the token (catch both expired and invalid)
            try:
                # validated_token = user_authenticator.get_validated_token(access_token)
                # user = user_authenticator.get_user(validated_token)
                # request.user = user
                validated_token = AccessToken(access_token)
                user = JWTAuthentication().get_user(validated_token)
                request.user = user
                print('token ', user)
            except (InvalidToken, TokenError):
                # Step 2: If access token is invalid/expired, try refreshing
                if refresh_token:
                    try:
                        new_token = RefreshToken(refresh_token).access_token
                        # Replace the token in META for DRF to pick it up
                        request.META['HTTP_AUTHORIZATION'] = f'Bearer {str(new_token)}'
                        request.new_access_token = str(new_token)

                        # Authenticate again using the new token
                        validated_token = user_authenticator.get_validated_token(new_token)
                        user = user_authenticator.get_user(validated_token)

                        request.user = user
                        request.new_access_token = str(new_token)
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
        if hasattr(request, 'new_access_token'):
            print('request.new_access_token :', request.new_access_token)
            response['X-New-Access-Token'] = request.new_access_token
        return response
    


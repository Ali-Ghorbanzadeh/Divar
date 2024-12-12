from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.exceptions import AuthenticationFailed
from django.utils.timezone import now


class TokenRefreshMiddleware:
    """
    Middleware for automatically refreshing JWT access token if expired.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get('Authorization')
        print(token)
        if token:
            token = token.replace('Bearer ', '')
            try:
                access_token = AccessToken(token)
                if access_token['exp'] < int(now().timestamp()):
                    refresh_token = request.headers.get('X-Refresh-Token')
                    if refresh_token:
                        refresh_token = RefreshToken(refresh_token)
                        new_access_token = str(refresh_token.access_token)
                        request.headers['Authorization'] = f'Bearer {new_access_token}'
                    else:
                        raise AuthenticationFailed('No refresh token available.')
            except Exception as e:
                raise AuthenticationFailed(f'Token validation failed: {str(e)}')

        response = self.get_response(request)
        return response

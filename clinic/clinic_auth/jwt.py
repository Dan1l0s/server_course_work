import jwt
from django.conf import settings
from rest_framework import authentication
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        request.user = None
        token = authentication.get_authorization_header(request)[7:]
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(pk=payload['id'])
            return (user, token)
        except Exception as e:
            print(e)
            return (None, token)

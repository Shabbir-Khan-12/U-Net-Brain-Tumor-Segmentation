import jwt
from rest_framework import permissions, exceptions
from django.conf import settings

class CustomJWTAuthorization(permissions.BasePermission):
    def has_permission(self, request, view):
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        if auth_header is None:
            return False

        try:
            token = auth_header.split(' ')[1]
            decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # Add your custom authorization logic here if needed
            return True
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Token is invalid')

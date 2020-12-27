import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User

class JWTAuthentication(authentication.BaseAuthentication):

    token_prefix = "Token"
    def authenticate(self, request):

        request.user = None # <- I am not sure why this is needed here

        # get token from http header.
        # key is Authorization
        # This program expect that value is composed prefix and token separated by whitespace
        # The element is binary type
        # The below code is wrapped inside authentication.get_authorization_header
        # request.META.get('HTTP_AUTHORIZATION', b'') 
        auth_header = authentication.get_authorization_header(request).split()
        
        # auth_header must be two length of list if the token format is right
        # if not, the method return None, and BaseAuthentication takes care of
        # error handling.
        if not auth_header or len(auth_header) == 1 or len(auth_header) > 2:
            return None
        
        # decode binary to utf-8 string
        # jwt decoder cannot process binary data
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != self.token_prefix.lower():
            return None

        return self._chack_token(request, token)

    def _chack_token(self, request, token):

        # Decode token
        # User model encode token by user id and expire date with settings.SECRET_KEY
        # Therefore, payload should have id and expire date as dictionary
        # if the decode succeeds
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = "Toekn is wrong"
            raise exceptions.AuthenticationFailed(msg)

        # payload should have id as dictionary
        # Check out if user is in Database and the user is active user
        try:
            user = User.objects.get(pk=payload["id"])
        except User.DoesNotExist:
            msg = "User does not exist"
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = "User is deleted"
            raise exceptions.AuthenticationFailed(msg)

        # All authentication process passed, return user and token as tulple
        return (user, token)



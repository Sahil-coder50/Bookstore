# authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class ZohoAPIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        # Expected format: Zoho-APIKey <key>
        try:
            prefix, key = auth_header.split()
        except ValueError:
            raise AuthenticationFailed("Invalid authorization header")

        if prefix != "Zoho-APIKey" or key != settings.ZOHO_API_KEY:
            raise AuthenticationFailed("Invalid API key")

        return (None, None)  # no user object needed if it's system-to-system

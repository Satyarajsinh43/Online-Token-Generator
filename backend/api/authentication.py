from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User, AnonymousUser
from clerk_backend_api import Clerk
import os
from django.conf import settings
import json
import base64

class ClerkAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        
        clerk_secret_key = getattr(settings, 'CLERK_SECRET_KEY', os.environ.get('CLERK_SECRET_KEY'))
        if not clerk_secret_key:
            return None
            
        try:
            def decode_base64_url(s):
                pad = len(s) % 4
                if pad:
                    s += '=' * (4 - pad)
                return base64.urlsafe_b64decode(s)
                
            parts = token.split('.')
            if len(parts) != 3:
                return None
            
            payload_json = decode_base64_url(parts[1]).decode('utf-8')
            unverified_payload = json.loads(payload_json)
            
            # Only process if it looks like a Clerk token, else let other auth backends handle it
            iss = unverified_payload.get('iss', '')
            if 'clerk' not in iss:
                return None
            
            clerk_user_id = unverified_payload.get('sub')
            if not clerk_user_id:
                raise AuthenticationFailed('Invalid Token Payload')
            
            clerk = Clerk(bearer_auth=clerk_secret_key)
            clerk_user = clerk.users.get(user_id=clerk_user_id)
            if not clerk_user:
                 raise AuthenticationFailed('Invalid Clerk User')
                 
            email = None
            for email_obj in clerk_user.email_addresses:
                if email_obj.id == clerk_user.primary_email_address_id:
                     email = email_obj.email_address
                     break
                     
            if not email and clerk_user.email_addresses:
                email = clerk_user.email_addresses[0].email_address
                
            if not email:
                raise AuthenticationFailed('No email found in Clerk User')
                     
            user = User.objects.filter(email=email).first()
            if user:
                return (user, token)
            else:
                # User hasn't synced yet. Return AnonymousUser so DRF considers the token valid 
                # but without an attached Django user profile yet.
                return (AnonymousUser(), token)
                
        except Exception as e:
            raise AuthenticationFailed(f'Invalid Clerk Token Error: {str(e)}')
            
    def authenticate_header(self, request):
        return 'Bearer'

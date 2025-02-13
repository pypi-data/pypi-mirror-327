from django.contrib.auth.backends import ModelBackend, BaseBackend
from django.contrib.auth.models import AnonymousUser
import uuid
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

class SessionEnhancingAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Override the authenticate method to add custom attributes to the session.
        """
        user = super().authenticate(request, username=username, password=password, **kwargs)

        if user and user.is_authenticated:
            # Set custom session attributes for authenticated user
            # extra_fields = ['is_active', 'is_superuser', 'is_staff', 'email', 'user_type']
            extra_fields = ['is_active', 'is_superuser', 'is_staff', 'email']
            existing_fields = [field for field in extra_fields if hasattr(user, field)]

            # map(lambda field: request.session.__setitem__(f"user_{field}", getattr(user, field)), existing_fields) # used map instead of for loop so I can practice using maps. But it does not actually set the items
            [request.session.__setitem__(f"user_{field}", getattr(user, field)) for field in existing_fields]

            request.session["account_type"] = settings.AUTH_IDENTIFIER
        
        return None

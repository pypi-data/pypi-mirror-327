# second_service/middleware.py
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

class SharedSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.User = get_user_model()
    
    def __call__(self, request):
        if request.session.get("_auth_user_id"):
            # Create a temporary user instance without database lookup
            user = self.User(
                id=request.session["_auth_user_id"],
                is_active=False,
                is_staff=False,
                is_superuser=False
            )
            # extra_fields = ['is_active', 'is_superuser', 'is_staff', 'email', 'user_type']
            extra_fields = ['is_active', 'is_superuser', 'is_staff', 'email']
            # set dditional attributes from session
            for field in extra_fields:
                session_field = f"user_{field}"
                if request.session.get(session_field):
                    setattr(user, field, request.session[session_field])
            request.user = user

        else:
            # # login_url = settings.AUTH_SERVICE_ROOT + '/admin'  # Redirect to the authentication service's login endpoint
            # login_url = settings.AUTH_SERVICE_ROOT + f'/admin/login/?next=/{settings.SERVICE_ROOT}admin/'
            # return redirect(login_url) # I'd like to redirect only if accessing admin, other endpoints should return anonymous user
            # request.user = AnonymousUser()

            # Define the admin URL using reverse lookup for the login page
            try:
                admin_login_url = reverse('admin:login')  # Use Django admin login URL
            except Exception as e:
                admin_login_url = settings.AUTH_SERVICE_ROOT + f'/admin/login/?next=/{settings.SERVICE_ROOT}admin/'

            # Check if the request path matches any admin URLs
            # You can use a URL pattern name or manually check the path for certain admin views.
            # Here, I'm assuming that if the request URL matches any admin-related pattern, it should redirect.
            if request.path.startswith(reverse('admin:login')) or 'admin' in request.path:
                login_url = settings.AUTH_SERVICE_ROOT + f'/admin/login/?next={request.path}'
                return HttpResponseRedirect(login_url)

            # For other endpoints, set an anonymous user
            request.user = AnonymousUser()

        return self.get_response(request)
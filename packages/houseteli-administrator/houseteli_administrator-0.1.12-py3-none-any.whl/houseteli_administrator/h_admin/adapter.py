from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import build_absolute_uri
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        origin = request.META.get('HTTP_ORIGIN', None)
        referer_host = request.META.get('HTTP_REFERER', None)
        # if referer_host:
        #     base_url = referer_host  # Use Referer as the base URL
        if origin:
            base_url = origin
        else:
            base_url = f"{request.scheme}://{request.get_host()}"
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        ret = f"{base_url}/users/verifyemail/?key={emailconfirmation.key}"
        return ret
    
    
    def send_mail(self, template_prefix, email, context):
        """
        Override to customize the password reset URL in the context.
        """
        request = context.get("request")
        if request:
            base_url = settings.FRONTEND_URL
            if base_url.endswith('/'):
                base_url = base_url[:-1]

            # Update the password reset URL in the context
            if "password_reset_url" in context:
                # print(context)
                context["password_reset_url"] = f"{base_url}/users/reset-password/?token={context['token']}&uid={context['uid']}"
        super().send_mail(template_prefix, email, context)
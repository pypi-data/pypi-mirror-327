from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    username = None
    email = serializers.EmailField(required=True)
    def custom_signup(self, request, user):
        user.email = self.data.get('email')
        user.save()


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.conf import settings
# from decouple import config
# account_type = config('ACCOUNTTYPE', default=None)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to add extra claims to the JWT.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_superuser'] = user.is_superuser
        # token['user_type'] = user.user_type
        return token

from django.shortcuts import render

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View that uses the custom serializer to return a JWT with extra claims.
    """
    serializer_class = CustomTokenObtainPairSerializer




from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount
from .serializers import EmailCheckSerializer

User = get_user_model() 

class BaseEmailCheckViewSet(ViewSet):

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            response_data = {
                "name": user.get_full_name() or user.username,
                "email": user.email,
            }

            # Check for social account
            social_account = SocialAccount.objects.filter(user=user).first()
            if social_account:
                response_data["social_providers"] = f"Social account ({social_account.provider})"
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailCheckViewSet(BaseEmailCheckViewSet):
    serializer_class = EmailCheckSerializer

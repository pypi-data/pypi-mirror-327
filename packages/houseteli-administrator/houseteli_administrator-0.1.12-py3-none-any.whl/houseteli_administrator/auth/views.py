from django.shortcuts import render

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View that uses the custom serializer to return a JWT with extra claims.
    """
    serializer_class = CustomTokenObtainPairSerializer
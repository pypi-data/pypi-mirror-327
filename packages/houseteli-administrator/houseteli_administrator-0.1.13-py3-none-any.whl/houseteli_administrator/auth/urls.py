# urls.py
from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="My API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myapi.local"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
)


from django.urls import path
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    # Endpoint to log in and obtain a new token pair (access and refresh tokens)
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Endpoint to refresh the access token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Endpoint to verify a token's validity
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
urlpatterns += [
    path('accounts/', include('allauth.urls')),
     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/auth/', include('dj_rest_auth.urls')),  # Login, Logout, Password Reset
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  # Registration
]
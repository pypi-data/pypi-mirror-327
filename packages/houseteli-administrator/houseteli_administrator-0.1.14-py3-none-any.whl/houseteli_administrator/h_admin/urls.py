# urls.py
from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# You can define your API view, or use the router for DRF views
# For example:
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

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
from .views import IdentityView
urlpatterns = [
    path('api/identity/', IdentityView.as_view(), name='identity'),
]
from rest_framework import serializers
from .models import Identity
from django.conf import settings


class IdentitySerializer(serializers.ModelSerializer):
    service_name = serializers.SerializerMethodField()
    service_root = serializers.SerializerMethodField()

    class Meta:
        model = Identity
        fields = ['name', 'service_type', 'enable_admin', 'description', 'service_name', 'service_root']  # Include extra fields

    def get_service_name(self, obj):
        return settings.SERVICE_NAME

    def get_service_root(self, obj):
        return settings.SERVICE_ROOT



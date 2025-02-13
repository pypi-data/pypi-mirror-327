from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html
from .models import Identity, ServiceType

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Display fields in the list view
    search_fields = ('name',)  # Add search functionality for the name field


@admin.register(Identity)
class IdentityAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'enable_admin', 'description', 'service_name_display', 'service_root_display')  # Show in list view
    readonly_fields = ('service_name_display', 'service_root_display')  # Make these fields uneditable in form view

    def has_add_permission(self, request):
        """Allow adding only if no Identity instance exists."""
        return not Identity.objects.exists()

    def service_name_display(self, obj):
        """Display SERVICE_NAME as a read-only field."""
        return format_html("<strong>{}</strong>", settings.SERVICE_NAME)
    service_name_display.short_description = "Service Name"

    def service_root_display(self, obj):
        """Display SERVICE_ROOT as a read-only field."""
        return format_html("<strong>{}</strong>", settings.SERVICE_ROOT)
    service_root_display.short_description = "Service Root"
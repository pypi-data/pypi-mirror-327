from django.core.management.base import BaseCommand
from houseteli_administrator.models import ServiceType, Identity
from django.conf import settings


class Command(BaseCommand):
    help = 'Create default ServiceType and Identity instance'

    def handle(self, *args, **kwargs):
        # Create the default 'auth' ServiceType if it doesn't exist
        service_type, created = ServiceType.objects.get_or_create(
            name='auth',
            defaults={'description': 'Authentication Service'}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS("Created default 'auth' ServiceType"))
        else:
            self.stdout.write(self.style.SUCCESS("'auth' ServiceType already exists"))
        
        # Check if the Identity instance exists, if not, create it
        if not Identity.objects.exists():
            identity_name = getattr(settings, 'SERVICE_NAME', 'anon')
            identity_description = f"{identity_name} Service"  # Custom description logic

            identity = Identity.objects.create(
                name=identity_name,
                description=identity_description,
                enable_admin=True,
                service_type=service_type
            )

            self.stdout.write(self.style.SUCCESS(f"Created Identity: {identity.name}"))
        else:
            self.stdout.write(self.style.SUCCESS("Identity instance already exists"))

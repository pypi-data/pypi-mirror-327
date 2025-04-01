from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import uuid


class ServiceType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Service Types"

class Identity(models.Model):
    AUTH='auth'
    name = models.CharField(max_length=255)
    description = models.TextField()
    TYPE_CHOICES = [
        (AUTH, 'auth'),
    ]

    # service_type = models.CharField(
    #     max_length=4,
    #     choices=TYPE_CHOICES,
    #     default=AUTH,
    #     editable=False
    # )
    service_type = models.ForeignKey(
        'ServiceType',
        on_delete=models.SET_NULL,
        null=True,
        editable=False
    )

    enable_admin = models.BooleanField(default=False, verbose_name="Enable Admin")

    def save(self, *args, **kwargs):
        if Identity.objects.exists() and not self.pk:
            raise ValidationError("Only one Identity instance is allowed.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Identity"
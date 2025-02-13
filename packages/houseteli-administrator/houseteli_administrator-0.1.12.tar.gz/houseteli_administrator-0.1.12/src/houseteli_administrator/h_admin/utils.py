from django.contrib import admin
from django.conf import settings
import textwrap

def set_site_id():
    max_length=12
    admin.site.site_title = f"{settings.SERVICE_NAME} site admin"
    admin.site.site_header = textwrap.shorten(f"{settings.SERVICE_NAME} administration", width=max_length, placeholder="...")
    admin.site.index_title = f"{settings.SERVICE_NAME} administration"

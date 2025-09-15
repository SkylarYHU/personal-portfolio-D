#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

print("=== Production Environment Check ===")
print(f"DEBUG: {settings.DEBUG}")
print(f"IS_DEVELOPMENT (env): {os.getenv('IS_DEVELOPMENT')}")
print(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', 'Not set')}")
print(f"AWS_STORAGE_BUCKET_NAME: {getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'Not set')}")
print(f"AWS_S3_CUSTOM_DOMAIN: {getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', 'Not set')}")
print(f"AWS_ACCESS_KEY_ID: {'Set' if getattr(settings, 'AWS_ACCESS_KEY_ID', None) else 'Not set'}")
print(f"AWS_SECRET_ACCESS_KEY: {'Set' if getattr(settings, 'AWS_SECRET_ACCESS_KEY', None) else 'Not set'}")
print(f"AWS_S3_REGION_NAME: {getattr(settings, 'AWS_S3_REGION_NAME', 'Not set')}")

# Check if we're using S3
if hasattr(settings, 'DEFAULT_FILE_STORAGE'):
    if 'S3' in settings.DEFAULT_FILE_STORAGE:
        print("\n✓ S3 storage is configured")
    else:
        print("\n✗ S3 storage is NOT configured")
        print(f"Current storage: {settings.DEFAULT_FILE_STORAGE}")

# Test media URL generation
try:
    from portfolioapp.models import Project
    project = Project.objects.first()
    if project and project.image:
        print(f"\nSample image URL: {project.image.url}")
except Exception as e:
    print(f"\nError getting sample image URL: {e}")
#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

print("=== Production Fix Verification ===")
print(f"DYNO environment variable: {os.getenv('DYNO')}")
print(f"IS_PRODUCTION detected: {getattr(settings, 'IS_PRODUCTION', 'Not set')}")
print(f"DEBUG: {settings.DEBUG}")
print(f"IS_DEVELOPMENT (env): {os.getenv('IS_DEVELOPMENT')}")
print(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
print(f"MEDIA_URL: {settings.MEDIA_URL}")

# Check if S3 is properly configured
if hasattr(settings, 'DEFAULT_FILE_STORAGE'):
    if 'S3' in settings.DEFAULT_FILE_STORAGE:
        print("\n✓ S3 storage is NOW configured correctly!")
        print(f"AWS_STORAGE_BUCKET_NAME: {getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'Not set')}")
        print(f"AWS_S3_CUSTOM_DOMAIN: {getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', 'Not set')}")
    else:
        print("\n✗ S3 storage is still NOT configured")
        print(f"Current storage: {settings.DEFAULT_FILE_STORAGE}")

# Test a sample image URL
try:
    from portfolioapp.models import Project
    project = Project.objects.first()
    if project and project.image:
        print(f"\nSample image URL: {project.image.url}")
        if 's3.amazonaws.com' in project.image.url:
            print("✓ Images are now served from S3!")
        else:
            print("✗ Images are still served locally")
except Exception as e:
    print(f"\nError getting sample image URL: {e}")
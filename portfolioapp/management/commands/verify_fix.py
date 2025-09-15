from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Verify production environment fix'

    def handle(self, *args, **options):
        self.stdout.write("=== Production Fix Verification ===")
        self.stdout.write(f"DYNO environment variable: {os.getenv('DYNO')}")
        self.stdout.write(f"IS_PRODUCTION detected: {getattr(settings, 'IS_PRODUCTION', 'Not set')}")
        self.stdout.write(f"DEBUG: {settings.DEBUG}")
        self.stdout.write(f"IS_DEVELOPMENT (env): {os.getenv('IS_DEVELOPMENT')}")
        self.stdout.write(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        self.stdout.write(f"MEDIA_URL: {settings.MEDIA_URL}")
        
        # Check if S3 is properly configured
        if hasattr(settings, 'DEFAULT_FILE_STORAGE'):
            if 'S3' in settings.DEFAULT_FILE_STORAGE:
                self.stdout.write(self.style.SUCCESS("\n✓ S3 storage is NOW configured correctly!"))
                self.stdout.write(f"AWS_STORAGE_BUCKET_NAME: {getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'Not set')}")
                self.stdout.write(f"AWS_S3_CUSTOM_DOMAIN: {getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', 'Not set')}")
            else:
                self.stdout.write(self.style.ERROR("\n✗ S3 storage is still NOT configured"))
                self.stdout.write(f"Current storage: {settings.DEFAULT_FILE_STORAGE}")
        
        # Test a sample image URL
        try:
            from portfolioapp.models import Project
            project = Project.objects.first()
            if project and project.image:
                self.stdout.write(f"\nSample image URL: {project.image.url}")
                if 's3.amazonaws.com' in project.image.url:
                    self.stdout.write(self.style.SUCCESS("✓ Images are now served from S3!"))
                else:
                    self.stdout.write(self.style.ERROR("✗ Images are still served locally"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\nError getting sample image URL: {e}"))
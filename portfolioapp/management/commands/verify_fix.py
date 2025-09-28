from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Verify production environment fix and repair category field'

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
            
        # Check and fix category field
        self.stdout.write("\n=== Category Field Check ===\n")
        self.stdout.write("Checking and fixing category field...")
        
        try:
            with connection.cursor() as cursor:
                # Check if category column exists
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='portfolioapp_socialmediapost' 
                    AND column_name='category';
                """)
                
                result = cursor.fetchone()
                
                if result:
                    self.stdout.write(self.style.SUCCESS("✓ Category field already exists"))
                else:
                    self.stdout.write("Adding category field...")
                    cursor.execute("""
                        ALTER TABLE portfolioapp_socialmediapost 
                        ADD COLUMN category VARCHAR(128) DEFAULT '';
                    """)
                    self.stdout.write(self.style.SUCCESS("✓ Category field added successfully"))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
            
        # Verify the field was added
        try:
            from portfolioapp.models import SocialMediaPost
            fields = [f.name for f in SocialMediaPost._meta.fields]
            if 'category' in fields:
                self.stdout.write(self.style.SUCCESS("✓ Category field is now available in the model"))
            else:
                self.stdout.write(self.style.ERROR("✗ Category field is still missing from the model"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error checking model: {e}"))
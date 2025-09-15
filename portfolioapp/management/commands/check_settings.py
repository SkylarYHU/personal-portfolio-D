from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Check Django settings in production'

    def handle(self, *args, **options):
        self.stdout.write(f"DEBUG: {settings.DEBUG}")
        self.stdout.write(f"MEDIA_URL: {settings.MEDIA_URL}")
        self.stdout.write(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'Not set')}")
        self.stdout.write(f"AWS_STORAGE_BUCKET_NAME: {getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'Not set')}")
        self.stdout.write(f"AWS_S3_CUSTOM_DOMAIN: {getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', 'Not set')}")
        self.stdout.write(f"IS_DEVELOPMENT: {getattr(settings, 'IS_DEVELOPMENT', 'Not set')}")
        
        # Check if we have all AWS settings
        aws_settings = [
            'AWS_ACCESS_KEY_ID',
            'AWS_SECRET_ACCESS_KEY', 
            'AWS_STORAGE_BUCKET_NAME',
            'AWS_S3_REGION_NAME'
        ]
        
        self.stdout.write("\nAWS Settings check:")
        for setting in aws_settings:
            value = getattr(settings, setting, None)
            if value:
                self.stdout.write(f"{setting}: {'*' * len(str(value))} (set)")
            else:
                self.stdout.write(f"{setting}: Not set")
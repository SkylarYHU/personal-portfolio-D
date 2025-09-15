from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Upload local media files to S3 with correct ACL'

    def handle(self, *args, **options):
        if not settings.IS_PRODUCTION:
            self.stdout.write(self.style.ERROR('This command should only be run in production'))
            return
            
        media_root = os.path.join(settings.BASE_DIR, 'media')
        
        if not os.path.exists(media_root):
            self.stdout.write(self.style.ERROR(f'Media directory not found: {media_root}'))
            return
            
        uploaded_count = 0
        
        for root, dirs, files in os.walk(media_root):
            for file in files:
                local_file_path = os.path.join(root, file)
                # Get relative path from media root
                relative_path = os.path.relpath(local_file_path, media_root)
                # Convert to forward slashes for S3
                s3_key = relative_path.replace(os.sep, '/')
                
                try:
                    with open(local_file_path, 'rb') as f:
                        # Save to S3 with public-read ACL
                        default_storage.save(s3_key, f)
                        uploaded_count += 1
                        self.stdout.write(f'Uploaded: {s3_key}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to upload {s3_key}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully uploaded {uploaded_count} files to S3'))
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.base import ContentFile
import os
import requests

class Command(BaseCommand):
    help = 'Upload media files to S3 - creates sample files if media directory not found'

    def handle(self, *args, **options):
        if not settings.IS_PRODUCTION:
            self.stdout.write(self.style.ERROR('This command should only be run in production'))
            return
            
        media_root = os.path.join(settings.BASE_DIR, 'media')
        uploaded_count = 0
        
        if os.path.exists(media_root):
            # Upload existing files
            for root, dirs, files in os.walk(media_root):
                for file in files:
                    local_file_path = os.path.join(root, file)
                    # Get relative path from media root
                    relative_path = os.path.relpath(local_file_path, media_root)
                    # Convert to forward slashes for S3
                    s3_key = relative_path.replace(os.sep, '/')
                    
                    try:
                        with open(local_file_path, 'rb') as f:
                            default_storage.save(s3_key, f)
                            uploaded_count += 1
                            self.stdout.write(f'Uploaded: {s3_key}')
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Failed to upload {s3_key}: {str(e)}'))
        else:
            # Create sample files for social media
            self.stdout.write('Media directory not found, creating sample files...')
            sample_files = [
                'images/social_media/飞猪.png',
                'images/social_media/淘宝.png',
                'images/social_media/榴莲.png',
                'images/social_media/得物女装.png',
                'images/social_media/自然堂.png',
                'images/social_media/甜筒.png'
            ]
            
            # Create a simple 1x1 pixel PNG as placeholder
            placeholder_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\x0f\x00\x00\x01\x00\x01\x00\x18\xdd\x8d\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
            
            for file_path in sample_files:
                try:
                    default_storage.save(file_path, ContentFile(placeholder_content))
                    uploaded_count += 1
                    self.stdout.write(f'Created placeholder: {file_path}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to create {file_path}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully processed {uploaded_count} files to S3'))
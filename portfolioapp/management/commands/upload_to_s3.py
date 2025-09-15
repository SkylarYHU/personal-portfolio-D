from django.core.management.base import BaseCommand
from django.conf import settings
import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

class Command(BaseCommand):
    help = 'Upload media files to AWS S3'

    def handle(self, *args, **options):
        if not all([settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_STORAGE_BUCKET_NAME]):
            self.stdout.write(
                self.style.ERROR('AWS credentials not configured. Please set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_STORAGE_BUCKET_NAME environment variables.')
            )
            return

        # Initialize S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        # Check if bucket exists
        try:
            s3_client.head_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
            self.stdout.write(f'Bucket {settings.AWS_STORAGE_BUCKET_NAME} exists.')
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                self.stdout.write(
                    self.style.ERROR(f'Bucket {settings.AWS_STORAGE_BUCKET_NAME} does not exist.')
                )
                return
            else:
                self.stdout.write(
                    self.style.ERROR(f'Error accessing bucket: {e}')
                )
                return

        media_root = settings.MEDIA_ROOT
        if not os.path.exists(media_root):
            self.stdout.write(
                self.style.WARNING(f'Media directory {media_root} does not exist.')
            )
            return

        uploaded_count = 0
        error_count = 0

        # Walk through media directory and upload files
        for root, dirs, files in os.walk(media_root):
            for file in files:
                if file.startswith('.'):  # Skip hidden files
                    continue
                    
                local_path = os.path.join(root, file)
                # Get relative path from media root
                relative_path = os.path.relpath(local_path, media_root)
                # Use forward slashes for S3 key
                s3_key = relative_path.replace(os.sep, '/')
                
                try:
                    # Check if file already exists in S3
                    try:
                        s3_client.head_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_key)
                        self.stdout.write(f'File {s3_key} already exists in S3, skipping.')
                        continue
                    except ClientError as e:
                        if int(e.response['Error']['Code']) != 404:
                            raise e
                    
                    # Upload file
                    s3_client.upload_file(
                        local_path,
                        settings.AWS_STORAGE_BUCKET_NAME,
                        s3_key
                    )
                    uploaded_count += 1
                    self.stdout.write(f'Uploaded: {s3_key}')
                    
                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'Error uploading {s3_key}: {e}')
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'Upload completed. {uploaded_count} files uploaded, {error_count} errors.'
            )
        )
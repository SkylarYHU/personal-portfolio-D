from django.core.management.base import BaseCommand
import boto3
import os
from botocore.exceptions import ClientError
from django.conf import settings

class Command(BaseCommand):
    help = 'Check S3 bucket configuration and permissions'

    def handle(self, *args, **options):
        try:
            # Initialize S3 client
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            self.stdout.write(f"Checking CORS configuration for bucket: {bucket_name}")
            
            # Get CORS configuration
            try:
                cors_config = s3_client.get_bucket_cors(Bucket=bucket_name)
                self.stdout.write("Current CORS configuration:")
                self.stdout.write(str(cors_config))
            except ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchCORSConfiguration':
                    self.stdout.write(self.style.WARNING("No CORS configuration found for this bucket"))
                else:
                    self.stdout.write(self.style.ERROR(f"Error getting CORS configuration: {e}"))
            
            # Check bucket policy
            try:
                policy = s3_client.get_bucket_policy(Bucket=bucket_name)
                self.stdout.write("\nBucket policy exists:")
                self.stdout.write(policy['Policy'])
            except ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
                    self.stdout.write(self.style.WARNING("\nNo bucket policy found"))
                else:
                    self.stdout.write(self.style.ERROR(f"\nError getting bucket policy: {e}"))
            
            # Check public access block
            try:
                public_access = s3_client.get_public_access_block(Bucket=bucket_name)
                self.stdout.write("\nPublic access block configuration:")
                self.stdout.write(str(public_access['PublicAccessBlockConfiguration']))
            except ClientError as e:
                self.stdout.write(self.style.ERROR(f"\nError getting public access block: {e}"))
            
            # Test a sample file URL
            sample_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/media/projects/sample.jpg"
            self.stdout.write(f"\nSample media URL format: {sample_url}")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
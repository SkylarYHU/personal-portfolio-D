#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

import boto3
from botocore.exceptions import ClientError

def upload_background_blur():
    """上传压缩后的background-blurs.png到S3"""
    
    # 检查是否在生产环境
    if not getattr(settings, 'IS_PRODUCTION', False):
        print("此脚本需要在生产环境配置下运行")
        print("请设置环境变量: IS_PRODUCTION=True")
        return
    
    # 文件路径
    local_file = 'media/images/background-blurs.png'
    s3_key = 'images/background-blurs.png'
    
    if not os.path.exists(local_file):
        print(f"文件不存在: {local_file}")
        return
    
    try:
        # 创建S3客户端
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        
        # 上传文件
        print(f"正在上传 {local_file} 到 S3...")
        s3_client.upload_file(
            local_file,
            settings.AWS_STORAGE_BUCKET_NAME,
            s3_key,
            ExtraArgs={
                'ContentType': 'image/png',
                'CacheControl': 'max-age=31536000'  # 1年缓存
            }
        )
        
        # 验证上传
        file_size = os.path.getsize(local_file)
        s3_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{s3_key}"
        
        print(f"✅ 上传成功!")
        print(f"   本地文件: {local_file} ({file_size:,} bytes)")
        print(f"   S3 URL: {s3_url}")
        
        # 如果有CloudFront，显示CDN URL
        if hasattr(settings, 'AWS_S3_CUSTOM_DOMAIN'):
            cdn_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_key}"
            print(f"   CDN URL: {cdn_url}")
            
    except ClientError as e:
        print(f"❌ S3上传失败: {e}")
    except Exception as e:
        print(f"❌ 上传过程中出错: {e}")

if __name__ == '__main__':
    upload_background_blur()
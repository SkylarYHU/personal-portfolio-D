#!/usr/bin/env python
"""
AWS S3配置测试脚本
使用方法: python test_s3_config.py
"""

import os
import sys
import django
from pathlib import Path

# 添加项目路径
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from django.conf import settings
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def test_s3_configuration():
    print("=== AWS S3配置测试 ===")
    print()
    
    # 检查环境变量
    print("1. 检查环境变量...")
    required_vars = [
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY', 
        'AWS_STORAGE_BUCKET_NAME',
        'AWS_S3_REGION_NAME'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = getattr(settings, var, None)
        if value:
            if var == 'AWS_SECRET_ACCESS_KEY':
                print(f"   ✅ {var}: {'*' * len(value)}")
            else:
                print(f"   ✅ {var}: {value}")
        else:
            print(f"   ❌ {var}: 未设置")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n❌ 缺少必要的环境变量: {', '.join(missing_vars)}")
        print("请参考 AWS_S3_SETUP.md 进行配置")
        return False
    
    print("\n2. 测试AWS凭证...")
    try:
        # 创建S3客户端
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        
        # 测试凭证
        s3_client.list_buckets()
        print("   ✅ AWS凭证有效")
        
    except NoCredentialsError:
        print("   ❌ AWS凭证无效")
        return False
    except ClientError as e:
        print(f"   ❌ AWS客户端错误: {e}")
        return False
    
    print("\n3. 检查S3存储桶...")
    try:
        # 检查存储桶是否存在
        s3_client.head_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        print(f"   ✅ 存储桶 '{settings.AWS_STORAGE_BUCKET_NAME}' 存在且可访问")
        
        # 列出存储桶中的一些对象
        response = s3_client.list_objects_v2(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            MaxKeys=5
        )
        
        if 'Contents' in response:
            print(f"   📁 存储桶中有 {len(response['Contents'])} 个文件（显示前5个）:")
            for obj in response['Contents']:
                print(f"      - {obj['Key']} ({obj['Size']} bytes)")
        else:
            print("   📁 存储桶为空")
            
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            print(f"   ❌ 存储桶 '{settings.AWS_STORAGE_BUCKET_NAME}' 不存在")
        elif error_code == 403:
            print(f"   ❌ 无权限访问存储桶 '{settings.AWS_STORAGE_BUCKET_NAME}'")
        else:
            print(f"   ❌ 存储桶访问错误: {e}")
        return False
    
    print("\n4. 检查Django配置...")
    if not settings.DEBUG:
        if hasattr(settings, 'DEFAULT_FILE_STORAGE'):
            print(f"   ✅ DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        print(f"   ✅ MEDIA_URL: {settings.MEDIA_URL}")
    else:
        print("   ℹ️  当前为开发模式，S3配置在生产环境中生效")
    
    print("\n✅ S3配置测试完成！")
    print("\n接下来的步骤:")
    print("1. 运行 'python manage.py upload_to_s3' 上传现有文件")
    print("2. 部署到生产环境测试")
    
    return True

if __name__ == '__main__':
    try:
        test_s3_configuration()
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        print("请检查配置并重试")
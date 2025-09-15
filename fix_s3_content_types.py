#!/usr/bin/env python
"""
修复S3存储桶中现有图片文件的Content-Type
"""

import os
import sys
import django
import boto3
import mimetypes
from botocore.exceptions import ClientError

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from django.conf import settings

def fix_s3_content_types():
    """修复S3存储桶中图片文件的Content-Type"""
    
    # 创建S3客户端
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    
    try:
        # 列出所有images/目录下的文件
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix='images/'
        )
        
        if 'Contents' not in response:
            print("没有找到任何文件")
            return
        
        files_fixed = 0
        
        for obj in response['Contents']:
            key = obj['Key']
            
            # 跳过目录
            if key.endswith('/'):
                continue
                
            # 获取当前文件的元数据
            try:
                head_response = s3_client.head_object(Bucket=bucket_name, Key=key)
                current_content_type = head_response.get('ContentType', '')
                
                # 根据文件扩展名猜测正确的Content-Type
                correct_content_type, _ = mimetypes.guess_type(key)
                
                if correct_content_type and current_content_type != correct_content_type:
                    print(f"修复文件: {key}")
                    print(f"  当前Content-Type: {current_content_type}")
                    print(f"  正确Content-Type: {correct_content_type}")
                    
                    # 复制文件到自身，但使用正确的Content-Type
                    copy_source = {'Bucket': bucket_name, 'Key': key}
                    
                    s3_client.copy_object(
                        CopySource=copy_source,
                        Bucket=bucket_name,
                        Key=key,
                        ContentType=correct_content_type,
                        MetadataDirective='REPLACE'
                    )
                    
                    files_fixed += 1
                    print(f"  ✓ 修复完成")
                else:
                    print(f"跳过文件: {key} (Content-Type已正确: {current_content_type})")
                    
            except ClientError as e:
                print(f"处理文件 {key} 时出错: {e}")
                continue
        
        print(f"\n修复完成！共修复了 {files_fixed} 个文件")
        
    except ClientError as e:
        print(f"访问S3时出错: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("开始修复S3文件的Content-Type...")
    success = fix_s3_content_types()
    if success:
        print("修复完成！")
    else:
        print("修复失败！")
        sys.exit(1)
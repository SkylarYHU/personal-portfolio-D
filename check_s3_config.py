#!/usr/bin/env python
import os
import django
from django.conf import settings
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

print("=== S3配置详细检查 ===\n")

# 1. 环境检查
print("1. 环境检查:")
print(f"   DEBUG: {settings.DEBUG}")
print(f"   IS_PRODUCTION: {getattr(settings, 'IS_PRODUCTION', '未设置')}")
print(f"   DYNO环境变量: {os.getenv('DYNO', '未设置')}")

# 2. S3配置检查
print("\n2. S3配置检查:")
aws_config = {
    'AWS_ACCESS_KEY_ID': getattr(settings, 'AWS_ACCESS_KEY_ID', None),
    'AWS_SECRET_ACCESS_KEY': getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
    'AWS_STORAGE_BUCKET_NAME': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None),
    'AWS_S3_CUSTOM_DOMAIN': getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None),
    'AWS_S3_REGION_NAME': getattr(settings, 'AWS_S3_REGION_NAME', None)
}

for key, value in aws_config.items():
    if key in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']:
        print(f"   {key}: {'✓ 已设置' if value else '✗ 未设置'}")
    else:
        print(f"   {key}: {value or '✗ 未设置'}")

# 3. Django存储配置
print("\n3. Django存储配置:")
print(f"   DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', '未设置')}")
print(f"   MEDIA_URL: {settings.MEDIA_URL}")
print(f"   MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', '未设置')}")

# 4. S3连接测试
print("\n4. S3连接测试:")
if all([aws_config['AWS_ACCESS_KEY_ID'], aws_config['AWS_SECRET_ACCESS_KEY'], aws_config['AWS_STORAGE_BUCKET_NAME']]):
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=aws_config['AWS_SECRET_ACCESS_KEY'],
            region_name=aws_config['AWS_S3_REGION_NAME'] or 'us-east-1'
        )
        
        # 测试存储桶访问
        try:
            s3_client.head_bucket(Bucket=aws_config['AWS_STORAGE_BUCKET_NAME'])
            print(f"   ✓ 存储桶 '{aws_config['AWS_STORAGE_BUCKET_NAME']}' 可访问")
            
            # 列出存储桶中的一些文件
            try:
                response = s3_client.list_objects_v2(
                    Bucket=aws_config['AWS_STORAGE_BUCKET_NAME'],
                    MaxKeys=10
                )
                if 'Contents' in response:
                    print(f"   ✓ 存储桶包含 {len(response['Contents'])} 个文件（显示前10个）:")
                    for obj in response['Contents'][:5]:
                        print(f"     - {obj['Key']}")
                else:
                    print("   ⚠️  存储桶为空")
            except Exception as e:
                print(f"   ✗ 列出文件失败: {e}")
                
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                print(f"   ✗ 存储桶 '{aws_config['AWS_STORAGE_BUCKET_NAME']}' 不存在")
            elif error_code == 403:
                print(f"   ✗ 无权限访问存储桶 '{aws_config['AWS_STORAGE_BUCKET_NAME']}'")
            else:
                print(f"   ✗ 存储桶访问错误: {e}")
                
    except Exception as e:
        print(f"   ✗ S3客户端初始化失败: {e}")
else:
    print("   ✗ S3配置不完整，跳过连接测试")

# 5. 测试图片URL生成
print("\n5. 图片URL测试:")
try:
    from portfolioapp.models import Project, SocialMediaPost
    
    # 测试Project图片
    project = Project.objects.first()
    if project and project.image:
        print(f"   项目图片URL: {project.image.url}")
        if 's3.amazonaws.com' in project.image.url or aws_config['AWS_S3_CUSTOM_DOMAIN'] in project.image.url:
            print("   ✓ 项目图片URL指向S3")
        else:
            print("   ✗ 项目图片URL仍指向本地")
    else:
        print("   ⚠️  没有找到项目图片")
    
    # 测试SocialMediaPost图片
    social_post = SocialMediaPost.objects.first()
    if social_post and social_post.mockup_image_1:
        print(f"   社交媒体图片URL: {social_post.mockup_image_1.url}")
        if 's3.amazonaws.com' in social_post.mockup_image_1.url or aws_config['AWS_S3_CUSTOM_DOMAIN'] in social_post.mockup_image_1.url:
            print("   ✓ 社交媒体图片URL指向S3")
        else:
            print("   ✗ 社交媒体图片URL仍指向本地")
    else:
        print("   ⚠️  没有找到社交媒体图片")
        
except Exception as e:
    print(f"   ✗ 图片URL测试失败: {e}")

# 6. 本地媒体文件检查
print("\n6. 本地媒体文件检查:")
media_root = getattr(settings, 'MEDIA_ROOT', '')
if os.path.exists(media_root):
    file_count = 0
    for root, dirs, files in os.walk(media_root):
        file_count += len([f for f in files if not f.startswith('.')])
    print(f"   ✓ 本地媒体文件夹存在，包含 {file_count} 个文件")
    
    # 检查关键图片文件
    key_files = [
        'images/social_media/飞猪.png',
        'images/social_media/淘宝.png',
        'images/branding',
        'images/mobile_landing'
    ]
    
    for key_file in key_files:
        full_path = os.path.join(media_root, key_file)
        if os.path.exists(full_path):
            if os.path.isfile(full_path):
                print(f"   ✓ 关键文件存在: {key_file}")
            else:
                file_count_in_dir = len([f for f in os.listdir(full_path) if not f.startswith('.')])
                print(f"   ✓ 关键目录存在: {key_file} ({file_count_in_dir} 个文件)")
        else:
            print(f"   ✗ 关键文件/目录缺失: {key_file}")
else:
    print(f"   ✗ 本地媒体文件夹不存在: {media_root}")

# 7. 问题诊断和建议
print("\n=== 问题诊断和解决建议 ===\n")

# 检查存储配置
if 'S3' not in getattr(settings, 'DEFAULT_FILE_STORAGE', ''):
    print("🚨 问题1: Django未配置使用S3存储")
    print("   解决方案: 确保在生产环境中 DEFAULT_FILE_STORAGE 设置为 S3 存储后端")
    print("")

# 检查AWS配置
if not all([aws_config['AWS_ACCESS_KEY_ID'], aws_config['AWS_SECRET_ACCESS_KEY'], aws_config['AWS_STORAGE_BUCKET_NAME']]):
    print("🚨 问题2: AWS配置不完整")
    print("   解决方案: 设置所有必需的AWS环境变量")
    print("")

# 检查自定义域名
if not aws_config['AWS_S3_CUSTOM_DOMAIN']:
    print("⚠️  建议: 设置 AWS_S3_CUSTOM_DOMAIN 以获得更好的URL")
    print("   建议值: your-bucket-name.s3.amazonaws.com")
    print("")

print("📋 下一步操作建议:")
print("1. 确认所有AWS环境变量在Heroku中正确设置")
print("2. 运行 'python manage.py upload_to_s3' 上传媒体文件")
print("3. 重新部署应用以应用S3配置")
print("4. 测试图片URL是否指向S3")
print("5. 检查S3存储桶的公共访问权限")

print("\n=== 检查完成 ===")
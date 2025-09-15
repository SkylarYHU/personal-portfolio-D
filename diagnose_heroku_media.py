#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

print("=== Heroku媒体文件问题诊断 ===\n")

# 1. 检查环境变量
print("1. 环境变量检查:")
print(f"   DEBUG: {settings.DEBUG}")
print(f"   IS_PRODUCTION: {getattr(settings, 'IS_PRODUCTION', '未设置')}")
print(f"   DYNO环境变量: {os.getenv('DYNO', '未设置')}")

# 2. 检查媒体文件配置
print("\n2. 媒体文件配置:")
print(f"   MEDIA_URL: {settings.MEDIA_URL}")
print(f"   MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', '未设置')}")
print(f"   DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', '未设置')}")

# 3. 检查AWS S3配置
print("\n3. AWS S3配置:")
aws_keys = {
    'AWS_ACCESS_KEY_ID': getattr(settings, 'AWS_ACCESS_KEY_ID', None),
    'AWS_SECRET_ACCESS_KEY': getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
    'AWS_STORAGE_BUCKET_NAME': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None),
    'AWS_S3_CUSTOM_DOMAIN': getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None),
    'AWS_S3_REGION_NAME': getattr(settings, 'AWS_S3_REGION_NAME', None)
}

for key, value in aws_keys.items():
    if key in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']:
        print(f"   {key}: {'已设置' if value else '未设置'}")
    else:
        print(f"   {key}: {value or '未设置'}")

# 4. 检查是否使用S3存储
print("\n4. 存储后端分析:")
if hasattr(settings, 'DEFAULT_FILE_STORAGE'):
    if 'S3' in settings.DEFAULT_FILE_STORAGE:
        print("   ✓ 正在使用S3存储")
    else:
        print(f"   ✗ 使用本地存储: {settings.DEFAULT_FILE_STORAGE}")
else:
    print("   ✗ DEFAULT_FILE_STORAGE未设置")

# 5. 测试数据库中的图片URL
print("\n5. 数据库图片URL测试:")
try:
    from portfolioapp.models import Project, SocialMediaPost
    
    # 测试Project图片
    project = Project.objects.first()
    if project and project.image:
        print(f"   项目图片URL: {project.image.url}")
        if 's3.amazonaws.com' in project.image.url or 'cloudfront' in project.image.url:
            print("   ✓ 图片URL指向S3/CDN")
        else:
            print("   ✗ 图片URL指向本地路径")
    
    # 测试SocialMediaPost图片
    social_post = SocialMediaPost.objects.first()
    if social_post and social_post.mockup_image_1:
        print(f"   社交媒体图片URL: {social_post.mockup_image_1.url}")
        if 's3.amazonaws.com' in social_post.mockup_image_1.url or 'cloudfront' in social_post.mockup_image_1.url:
            print("   ✓ 社交媒体图片URL指向S3/CDN")
        else:
            print("   ✗ 社交媒体图片URL指向本地路径")
            
except Exception as e:
    print(f"   错误: {e}")

# 6. 问题诊断和建议
print("\n=== 问题诊断和解决建议 ===\n")

# 检查是否在生产环境但未使用S3
if (os.getenv('DYNO') or getattr(settings, 'IS_PRODUCTION', False)) and not ('S3' in getattr(settings, 'DEFAULT_FILE_STORAGE', '')):
    print("🚨 主要问题: Heroku生产环境未配置S3存储")
    print("\n原因分析:")
    print("   - Heroku使用临时文件系统，每24小时重启时会清除所有上传的媒体文件")
    print("   - 当前配置使用本地存储，导致图片在dyno重启后丢失")
    
    print("\n解决方案:")
    print("   1. 配置AWS S3存储桶")
    print("   2. 设置Heroku环境变量:")
    print("      - AWS_ACCESS_KEY_ID")
    print("      - AWS_SECRET_ACCESS_KEY")
    print("      - AWS_STORAGE_BUCKET_NAME")
    print("      - AWS_S3_CUSTOM_DOMAIN")
    print("   3. 上传现有媒体文件到S3")
    print("   4. 重新部署应用")
    
elif 'S3' in getattr(settings, 'DEFAULT_FILE_STORAGE', ''):
    print("✓ S3存储已配置")
    if not all([aws_keys['AWS_ACCESS_KEY_ID'], aws_keys['AWS_SECRET_ACCESS_KEY'], aws_keys['AWS_STORAGE_BUCKET_NAME']]):
        print("🚨 问题: S3配置不完整")
        print("   请检查AWS环境变量是否正确设置")
    else:
        print("   S3配置看起来正常，可能需要检查:")
        print("   - S3存储桶权限设置")
        print("   - 媒体文件是否已上传到S3")
        print("   - 网络连接问题")
else:
    print("⚠️  开发环境: 使用本地存储")
    print("   这在本地开发中是正常的，但部署到Heroku时需要S3")

print("\n=== 诊断完成 ===")
#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from portfolioapp.models import Project, SocialMediaPost, BrandingProject, MobileLandingPage

print("=== 检查数据库中的媒体文件 ===")

# 检查Project模型
projects = Project.objects.all()
print(f"\nProject模型 ({projects.count()}个记录):")
for p in projects:
    if p.image:
        print(f"  - {p.title}: {p.image.name}")
        file_path = os.path.join(settings.MEDIA_ROOT, p.image.name)
        exists = os.path.exists(file_path)
        print(f"    文件存在: {exists}")
        if exists:
            print(f"    文件路径: {file_path}")

# 检查SocialMediaPost模型
social_posts = SocialMediaPost.objects.all()
print(f"\nSocialMediaPost模型 ({social_posts.count()}个记录):")
for sp in social_posts:
    for i, img_field in enumerate([sp.mockup_image_1, sp.mockup_image_2, sp.mockup_image_3], 1):
        if img_field:
            print(f"  - {sp.title} (图片{i}): {img_field.name}")
            file_path = os.path.join(settings.MEDIA_ROOT, img_field.name)
            exists = os.path.exists(file_path)
            print(f"    文件存在: {exists}")
            if exists:
                print(f"    文件路径: {file_path}")

# 检查BrandingProject模型
branding_projects = BrandingProject.objects.all()
print(f"\nBrandingProject模型 ({branding_projects.count()}个记录):")
for bp in branding_projects:
    for field_name in ['mockup_image_1', 'mockup_image_2', 'mockup_image_3', 'mockup_image_4', 'mockup_image_5']:
        img_field = getattr(bp, field_name, None)
        if img_field:
            print(f"  - {bp.title} ({field_name}): {img_field.name}")
            file_path = os.path.join(settings.MEDIA_ROOT, img_field.name)
            exists = os.path.exists(file_path)
            print(f"    文件存在: {exists}")
            if exists:
                print(f"    文件路径: {file_path}")

# 检查MobileLandingPage模型
mobile_pages = MobileLandingPage.objects.all()
print(f"\nMobileLandingPage模型 ({mobile_pages.count()}个记录):")
for mp in mobile_pages:
    for field_name in ['mockup_image_1', 'mockup_image_2', 'mockup_image_3']:
        img_field = getattr(mp, field_name, None)
        if img_field:
            print(f"  - {mp.title} ({field_name}): {img_field.name}")
            file_path = os.path.join(settings.MEDIA_ROOT, img_field.name)
            exists = os.path.exists(file_path)
            print(f"    文件存在: {exists}")
            if exists:
                print(f"    文件路径: {file_path}")

print(f"\n=== 配置信息 ===")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"DEBUG: {settings.DEBUG}")
print(f"IS_PRODUCTION: {getattr(settings, 'IS_PRODUCTION', 'Not set')}")
print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'Not set')}")

# 检查媒体文件夹是否存在
if os.path.exists(settings.MEDIA_ROOT):
    print(f"\n=== 媒体文件夹内容 ===")
    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        level = root.replace(settings.MEDIA_ROOT, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")
else:
    print(f"\n媒体文件夹不存在: {settings.MEDIA_ROOT}")
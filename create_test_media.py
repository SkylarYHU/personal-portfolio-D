#!/usr/bin/env python
import os
from PIL import Image, ImageDraw, ImageFont

# 创建媒体文件夹结构
base_dir = os.path.dirname(os.path.abspath(__file__))
media_dirs = [
    'media/images/social_media',
    'media/images/branding', 
    'media/images/mobile_landing',
    'media/images'
]

for dir_path in media_dirs:
    full_path = os.path.join(base_dir, dir_path)
    os.makedirs(full_path, exist_ok=True)
    print(f"创建目录: {full_path}")

# 创建一个测试图片
def create_test_image(filename, text="Test Image", size=(800, 600)):
    # 创建一个彩色背景的图片
    img = Image.new('RGB', size, color=(70, 130, 180))  # 钢蓝色背景
    draw = ImageDraw.Draw(img)
    
    # 尝试使用系统字体，如果没有就使用默认字体
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # 计算文字位置（居中）
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # 绘制文字
    draw.text((x, y), text, fill=(255, 255, 255), font=font)
    
    # 保存图片
    img.save(filename)
    print(f"创建测试图片: {filename}")

# 创建测试图片
test_images = [
    ('media/images/social_media/飞猪.png', '飞猪 Social Media'),
    ('media/images/social_media/test1.png', 'Social Media Test 1'),
    ('media/images/social_media/test2.png', 'Social Media Test 2'),
    ('media/images/branding/test_brand.png', 'Branding Test'),
    ('media/images/mobile_landing/test_mobile.png', 'Mobile Landing Test'),
    ('media/images/test_project.png', 'Project Test')
]

for img_path, img_text in test_images:
    full_path = os.path.join(base_dir, img_path)
    create_test_image(full_path, img_text)

print("\n测试媒体文件创建完成！")
print("\n媒体文件夹结构:")
for root, dirs, files in os.walk(os.path.join(base_dir, 'media')):
    level = root.replace(os.path.join(base_dir, 'media'), '').count(os.sep)
    indent = ' ' * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        print(f"{subindent}{file}")
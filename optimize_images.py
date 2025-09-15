#!/usr/bin/env python
"""
图片优化脚本 - 压缩现有图片以提升加载速度
使用方法: python optimize_images.py
"""

import os
import sys
from PIL import Image
import glob
from pathlib import Path

def optimize_image(image_path, quality=85, max_width=1920):
    """
    优化单个图片文件
    
    Args:
        image_path: 图片文件路径
        quality: JPEG质量 (1-100)
        max_width: 最大宽度像素
    """
    try:
        with Image.open(image_path) as img:
            # 获取原始信息
            original_size = os.path.getsize(image_path)
            original_width, original_height = img.size
            
            # 转换为RGB模式（如果需要）
            if img.mode in ('RGBA', 'LA', 'P'):
                # 创建白色背景
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 调整尺寸（如果需要）
            if original_width > max_width:
                ratio = max_width / original_width
                new_height = int(original_height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                print(f"  调整尺寸: {original_width}x{original_height} -> {max_width}x{new_height}")
            
            # 保存优化后的图片
            img.save(image_path, 'JPEG', quality=quality, optimize=True, progressive=True)
            
            # 计算压缩效果
            new_size = os.path.getsize(image_path)
            compression_ratio = (1 - new_size / original_size) * 100
            
            print(f"  原始大小: {original_size:,} bytes")
            print(f"  优化后: {new_size:,} bytes")
            print(f"  压缩率: {compression_ratio:.1f}%")
            
            return True
            
    except Exception as e:
        print(f"  错误: {e}")
        return False

def optimize_static_images():
    """
    优化static目录中的图片
    """
    print("=== 优化静态图片文件 ===")
    
    static_dir = Path('static/images')
    if not static_dir.exists():
        print("static/images 目录不存在")
        return
    
    # 支持的图片格式
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']
    
    total_original = 0
    total_optimized = 0
    optimized_count = 0
    
    for extension in image_extensions:
        for image_path in static_dir.glob(extension):
            print(f"\n优化: {image_path.name}")
            
            original_size = image_path.stat().st_size
            total_original += original_size
            
            if optimize_image(str(image_path)):
                optimized_size = image_path.stat().st_size
                total_optimized += optimized_size
                optimized_count += 1
    
    if optimized_count > 0:
        total_compression = (1 - total_optimized / total_original) * 100
        print(f"\n=== 优化完成 ===")
        print(f"优化文件数: {optimized_count}")
        print(f"总原始大小: {total_original:,} bytes ({total_original/1024/1024:.1f} MB)")
        print(f"总优化后: {total_optimized:,} bytes ({total_optimized/1024/1024:.1f} MB)")
        print(f"总压缩率: {total_compression:.1f}%")
        print(f"节省空间: {(total_original-total_optimized):,} bytes ({(total_original-total_optimized)/1024/1024:.1f} MB)")
    else:
        print("没有找到需要优化的图片文件")

def create_webp_versions():
    """
    为现有图片创建WebP版本（更小的文件大小）
    """
    print("\n=== 创建WebP版本 ===")
    
    static_dir = Path('static/images')
    if not static_dir.exists():
        return
    
    webp_count = 0
    
    for image_path in static_dir.glob('*.jpg'):
        webp_path = image_path.with_suffix('.webp')
        
        try:
            with Image.open(image_path) as img:
                # 转换为WebP格式
                img.save(str(webp_path), 'WEBP', quality=80, method=6)
                
                original_size = image_path.stat().st_size
                webp_size = webp_path.stat().st_size
                compression = (1 - webp_size / original_size) * 100
                
                print(f"创建: {webp_path.name} (压缩 {compression:.1f}%)")
                webp_count += 1
                
        except Exception as e:
            print(f"WebP转换失败 {image_path.name}: {e}")
    
    print(f"创建了 {webp_count} 个WebP文件")

def main():
    print("图片优化工具")
    print("=" * 50)
    
    # 检查PIL是否可用
    try:
        from PIL import Image
    except ImportError:
        print("错误: 需要安装Pillow库")
        print("运行: pip install Pillow")
        return
    
    # 优化现有图片
    optimize_static_images()
    
    # 创建WebP版本
    create_webp_versions()
    
    print("\n=== 后续建议 ===")
    print("1. 配置CloudFront CDN (参考 setup_cloudfront_cdn.md)")
    print("2. 在模板中使用WebP格式 (支持的浏览器)")
    print("3. 实现图片懒加载")
    print("4. 使用响应式图片 (srcset)")

if __name__ == '__main__':
    main()
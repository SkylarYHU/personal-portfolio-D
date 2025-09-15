#!/usr/bin/env python3
"""
Advanced image optimization script for better web performance
This will create multiple optimized versions of images
"""

import os
from PIL import Image, ImageFilter
import subprocess

def optimize_background_image():
    """Create highly optimized versions of background image"""
    input_path = "media/images/background-blurs.png"
    
    if not os.path.exists(input_path):
        print(f"❌ Input file not found: {input_path}")
        return
    
    # Open original image
    with Image.open(input_path) as img:
        print(f"📊 Original image: {img.size[0]}x{img.size[1]}, Mode: {img.mode}")
        
        # Convert to RGB if needed
        if img.mode in ('RGBA', 'LA'):
            # Create a white background
            background = Image.new('RGB', img.size, (15, 23, 42))  # #0f172a color
            if img.mode == 'RGBA':
                background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
            else:
                background.paste(img)
            img = background
        
        # Create different optimized versions
        versions = [
            {
                'name': 'background-blurs-optimized.jpg',
                'size': (1920, 1080),
                'quality': 85,
                'format': 'JPEG'
            },
            {
                'name': 'background-blurs-mobile.jpg', 
                'size': (1080, 720),
                'quality': 80,
                'format': 'JPEG'
            },
            {
                'name': 'background-blurs-webp.webp',
                'size': (1920, 1080), 
                'quality': 80,
                'format': 'WEBP'
            }
        ]
        
        for version in versions:
            # Resize image
            resized = img.copy()
            resized.thumbnail(version['size'], Image.Resampling.LANCZOS)
            
            # Apply slight blur for better compression
            if 'blur' in input_path:
                resized = resized.filter(ImageFilter.GaussianBlur(radius=0.5))
            
            # Save optimized version
            output_path = f"static/images/{version['name']}"
            
            save_kwargs = {
                'format': version['format'],
                'optimize': True
            }
            
            if version['format'] in ['JPEG', 'WEBP']:
                save_kwargs['quality'] = version['quality']
                
            if version['format'] == 'JPEG':
                save_kwargs['progressive'] = True
                
            resized.save(output_path, **save_kwargs)
            
            # Get file size
            size_kb = os.path.getsize(output_path) / 1024
            print(f"✅ Created {version['name']}: {resized.size[0]}x{resized.size[1]}, {size_kb:.1f}KB")

def create_responsive_css():
    """Create CSS for responsive background images"""
    css_content = """
/* 响应式背景图片优化 */
@media (max-width: 768px) {
  body {
    background-image: url("../images/background-blurs-mobile.jpg");
  }
}

@media (min-width: 769px) {
  body {
    background-image: url("../images/background-blurs-optimized.jpg");
  }
}

/* WebP支持检测 */
@supports (background-image: url("image.webp")) {
  body {
    background-image: url("../images/background-blurs-webp.webp");
  }
  
  @media (max-width: 768px) {
    body {
      background-image: url("../images/background-blurs-webp.webp");
    }
  }
}

/* 预加载优化 */
.preload-images {
  position: absolute;
  top: -9999px;
  left: -9999px;
  width: 1px;
  height: 1px;
  overflow: hidden;
}

.preload-images::after {
  content: url("../images/background-blurs-optimized.jpg") url("../images/background-blurs-mobile.jpg");
}
"""
    
    with open("static/css/responsive-images.css", "w") as f:
        f.write(css_content)
    
    print("✅ Created responsive-images.css")

if __name__ == "__main__":
    print("🚀 Starting advanced image optimization...")
    optimize_background_image()
    create_responsive_css()
    print("\n🎉 Optimization complete!")
    print("\n📝 Next steps:")
    print("1. Add responsive-images.css to your HTML")
    print("2. Test the optimized images")
    print("3. Deploy to production")
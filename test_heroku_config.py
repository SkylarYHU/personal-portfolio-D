#!/usr/bin/env python
import requests
import json

print("=== 测试Heroku应用配置 ===\n")

# 测试应用是否运行
print("1. 测试应用状态:")
try:
    response = requests.get('https://skylar-portfolio-2024.herokuapp.com/', timeout=10)
    print(f"   ✓ 应用响应状态: {response.status_code}")
except Exception as e:
    print(f"   ✗ 应用无法访问: {e}")

# 测试媒体文件URL
print("\n2. 测试媒体文件访问:")
media_urls = [
    'https://skylar-portfolio-2024.herokuapp.com/media/images/social_media/飞猪.png',
    'https://skylar-portfolio-media-2024.s3.eu-north-1.amazonaws.com/images/social_media/飞猪.png'
]

for url in media_urls:
    try:
        response = requests.head(url, timeout=10)
        print(f"   {url}")
        print(f"   状态: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✓ 可访问")
        elif response.status_code == 302:
            print(f"   → 重定向到: {response.headers.get('Location', '未知')}")
        else:
            print(f"   ✗ 无法访问")
        print()
    except Exception as e:
        print(f"   ✗ 请求失败: {e}\n")

# 测试API端点（如果有的话）
print("3. 测试配置信息:")
try:
    # 尝试访问一个可能暴露配置信息的端点
    response = requests.get('https://skylar-portfolio-2024.herokuapp.com/admin/', timeout=10)
    print(f"   管理页面状态: {response.status_code}")
except Exception as e:
    print(f"   管理页面测试失败: {e}")

print("\n=== 测试完成 ===")
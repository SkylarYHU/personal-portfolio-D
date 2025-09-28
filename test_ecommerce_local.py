#!/usr/bin/env python
import os
import sys
import django
from django.test import Client
from django.urls import reverse

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from portfolioapp.models import EcommerceProject

def test_ecommerce_detail():
    print('🧪 测试 E-commerce 详情页...')
    
    # 获取所有 ecommerce 项目
    ecommerce_projects = EcommerceProject.objects.all()
    print(f'📊 找到 {ecommerce_projects.count()} 个 E-commerce 项目')
    
    if not ecommerce_projects.exists():
        print('❌ 没有找到 E-commerce 项目数据')
        return
    
    # 创建测试客户端
    client = Client()
    
    for project in ecommerce_projects:
        print(f'\n🔍 测试项目: {project.title} (ID: {project.id})')
        
        try:
            # 测试详情页URL
            url = reverse('ecommerce_detail', args=[project.id])
            print(f'📍 URL: {url}')
            
            response = client.get(url)
            print(f'📊 响应状态码: {response.status_code}')
            
            if response.status_code == 200:
                print('✅ 页面加载成功')
                # 检查响应内容
                content = response.content.decode('utf-8')
                if project.title in content:
                    print('✅ 页面包含项目标题')
                else:
                    print('⚠️ 页面不包含项目标题')
            else:
                print(f'❌ 页面加载失败，状态码: {response.status_code}')
                if hasattr(response, 'context') and response.context:
                    print(f'🔍 上下文: {response.context}')
                    
        except Exception as e:
            print(f'❌ 测试失败: {e}')
            import traceback
            traceback.print_exc()
    
    # 测试首页是否能正常显示 ecommerce 项目
    print('\n🏠 测试首页 E-commerce 项目显示...')
    try:
        response = client.get('/')
        print(f'📊 首页响应状态码: {response.status_code}')
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            if 'ecommerce' in content.lower():
                print('✅ 首页包含 E-commerce 相关内容')
            else:
                print('⚠️ 首页不包含 E-commerce 相关内容')
        else:
            print(f'❌ 首页加载失败，状态码: {response.status_code}')
            
    except Exception as e:
        print(f'❌ 首页测试失败: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_ecommerce_detail()
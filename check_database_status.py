#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from portfolioapp.models import EcommerceProject, Project, BrandingProject, SocialMediaPost, MobileLandingPage, PowerPointPresentation
from django.db import connection

def check_database_status():
    print('🔍 检查数据库状态...')
    
    # 检查各个模型的数据数量
    models = [
        ('Project', Project),
        ('BrandingProject', BrandingProject),
        ('SocialMediaPost', SocialMediaPost),
        ('MobileLandingPage', MobileLandingPage),
        ('EcommerceProject', EcommerceProject),
        ('PowerPointPresentation', PowerPointPresentation)
    ]
    
    for model_name, model_class in models:
        try:
            count = model_class.objects.count()
            print(f'📊 {model_name}: {count} 条记录')
            
            if count > 0:
                # 显示前几条记录的ID和标题
                for obj in model_class.objects.all()[:3]:
                    print(f'   - ID: {obj.id}, Title: {obj.title}')
                    
        except Exception as e:
            print(f'❌ {model_name} 查询失败: {e}')
    
    # 检查数据库表结构
    print('\n🔍 检查数据库表结构...')
    with connection.cursor() as cursor:
        # 检查 portfolioapp_ecommerceproject 表是否存在
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name LIKE 'portfolioapp_%';
        """)
        
        tables = cursor.fetchall()
        print('📋 现有表:')
        for table in tables:
            print(f'   - {table[0]}')
            
        # 检查 ecommerce 表的字段
        if ('portfolioapp_ecommerceproject',) in tables:
            cursor.execute("PRAGMA table_info(portfolioapp_ecommerceproject);")
            columns = cursor.fetchall()
            print('\n📋 EcommerceProject 表字段:')
            for col in columns:
                print(f'   - {col[1]} ({col[2]})')

if __name__ == '__main__':
    check_database_status()
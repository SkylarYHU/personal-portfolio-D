#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from django.db.migrations.recorder import MigrationRecorder
from django.db import connection

def fix_migration_conflict():
    print('🚀 开始修复Heroku迁移冲突...')
    
    recorder = MigrationRecorder(connection)
    
    # 检查当前已应用的迁移
    applied_migrations = recorder.applied_migrations()
    portfolioapp_migrations = [m for m in applied_migrations if m[0] == 'portfolioapp']
    
    print('\n📋 当前已应用的portfolioapp迁移:')
    for migration in sorted(portfolioapp_migrations):
        print(f'  - {migration[1]}')
    
    # 需要标记为已应用的迁移
    target_migration = '0012_remove_socialmediapost_mockup_image_1_and_more'
    
    if ('portfolioapp', target_migration) not in applied_migrations:
        print(f'\n📝 标记迁移为已应用: {target_migration}')
        recorder.record_applied('portfolioapp', target_migration)
        print('✅ 迁移已标记为应用')
    else:
        print(f'\n✅ 迁移 {target_migration} 已经标记为应用')
    
    # 检查字段是否存在
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'portfolioapp_mobilelandingpage' 
            AND column_name = 'landing_pages_image';
        """)
        
        field_exists = cursor.fetchone() is not None
        print(f'\n🔍 landing_pages_image 字段存在: {field_exists}')
    
    print('\n🎉 迁移修复完成！')
    print('现在可以重新部署应用了。')

if __name__ == '__main__':
    fix_migration_conflict()
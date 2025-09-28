import os
import django
from django.conf import settings
from django.db import connection

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_portfolio.settings')
django.setup()

def check_landing_pages_image_field():
    """检查landing_pages_image字段是否存在"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='portfolioapp_mobilelandingpage' 
            AND column_name='landing_pages_image'
        """)
        result = cursor.fetchall()
        if result:
            print("字段 'landing_pages_image' 存在于表 'portfolioapp_mobilelandingpage' 中")
        else:
            print("字段 'landing_pages_image' 不存在于表 'portfolioapp_mobilelandingpage' 中")

if __name__ == "__main__":
    check_landing_pages_image_field()
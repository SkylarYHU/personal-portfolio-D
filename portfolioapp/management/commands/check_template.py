import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = '检查电商详情页模板文件'

    def handle(self, *args, **options):
        template_path = 'portfolioapp/templates/portfolioapp/ecommerce_detail.html'
        
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            self.stdout.write(f"模板文件总行数: {len(lines)}")
            
            # 检查所有模板标签
            for i, line in enumerate(lines):
                if '{%' in line:
                    self.stdout.write(f"第 {i+1} 行: {line.strip()}")
                    
            # 特别检查第155行附近
            start_line = max(0, 155-5)
            end_line = min(len(lines), 155+5)
            self.stdout.write(f"\n第155行附近的代码:")
            for i in range(start_line, end_line):
                marker = ">>> " if i == 154 else "    "
                self.stdout.write(f"{marker}{i+1}: {lines[i].rstrip()}")
        else:
            self.stdout.write(f"模板文件不存在: {template_path}")
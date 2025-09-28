#!/usr/bin/env python
# -*- coding: utf-8 -*-

def check_template():
    template_path = 'portfolioapp/templates/portfolioapp/ecommerce_detail.html'
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        print(f"模板文件总行数: {len(lines)}")
        
        # 检查所有模板标签
        print("\n所有模板标签:")
        for i, line in enumerate(lines):
            if '{%' in line:
                print(f"第 {i+1} 行: {line.strip()}")
                
        # 特别检查第155行附近
        print(f"\n第155行附近的代码:")
        start_line = max(0, 155-5)
        end_line = min(len(lines), 155+5)
        for i in range(start_line, end_line):
            marker = ">>> " if i == 154 else "    "
            print(f"{marker}{i+1}: {lines[i].rstrip()}")
            
        # 检查是否有未闭合的标签
        print(f"\n检查未闭合的标签:")
        if_count = 0
        endif_count = 0
        for i, line in enumerate(lines):
            if '{% if ' in line:
                if_count += 1
            if '{% endif %}' in line:
                endif_count += 1
                
        print(f"if标签数量: {if_count}")
        print(f"endif标签数量: {endif_count}")
        if if_count != endif_count:
            print(f"警告: if和endif标签数量不匹配!")
            
    except FileNotFoundError:
        print(f"模板文件不存在: {template_path}")
    except Exception as e:
        print(f"检查模板时出错: {e}")

if __name__ == "__main__":
    check_template()
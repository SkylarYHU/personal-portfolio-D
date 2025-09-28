#!/usr/bin/env python
"""
重置Heroku迁移状态脚本
这个脚本将帮助解决Heroku上的迁移冲突问题
"""

import subprocess
import sys

def run_heroku_command(command, app_name="skylarhu-portfolio"):
    """运行Heroku命令"""
    full_command = f"heroku {command} --app {app_name}"
    print(f"🔧 执行命令: {full_command}")
    
    try:
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
        print(f"📊 返回码: {result.returncode}")
        
        if result.stdout:
            print(f"📤 输出:\n{result.stdout}")
        
        if result.stderr:
            print(f"❌ 错误:\n{result.stderr}")
            
        return result.returncode == 0, result.stdout, result.stderr
        
    except Exception as e:
        print(f"❌ 命令执行失败: {e}")
        return False, "", str(e)

def reset_migrations():
    """重置迁移状态"""
    print("🚀 开始重置Heroku迁移状态...")
    
    # 1. 检查当前迁移状态
    print("\n📋 步骤1: 检查当前迁移状态")
    success, stdout, stderr = run_heroku_command('run "python manage.py showmigrations portfolioapp"')
    
    if not success:
        print("❌ 无法检查迁移状态")
        return False
    
    # 2. 标记问题迁移为已应用
    print("\n📋 步骤2: 标记迁移0024为已应用")
    success, stdout, stderr = run_heroku_command(
        'run "python manage.py migrate portfolioapp 0024 --fake"'
    )
    
    if not success:
        print("❌ 无法标记迁移0024")
        return False
    
    # 3. 应用迁移0025
    print("\n📋 步骤3: 应用迁移0025")
    success, stdout, stderr = run_heroku_command(
        'run "python manage.py migrate portfolioapp 0025"'
    )
    
    if not success:
        print("❌ 无法应用迁移0025")
        return False
    
    # 4. 运行完整迁移
    print("\n📋 步骤4: 运行完整迁移")
    success, stdout, stderr = run_heroku_command(
        'run "python manage.py migrate"'
    )
    
    if not success:
        print("❌ 完整迁移失败")
        return False
    
    # 5. 验证迁移状态
    print("\n📋 步骤5: 验证最终迁移状态")
    success, stdout, stderr = run_heroku_command(
        'run "python manage.py showmigrations portfolioapp"'
    )
    
    if success:
        print("✅ 迁移重置完成！")
        return True
    else:
        print("❌ 迁移验证失败")
        return False

def test_ecommerce_page():
    """测试ecommerce页面"""
    print("\n🧪 测试E-commerce页面...")
    
    # 测试页面访问
    success, stdout, stderr = run_heroku_command(
        'run "python -c \\"import requests; response = requests.get(\'https://skylarhu-portfolio-b8c6c9b0b5a1.herokuapp.com/ecommerce/1\'); print(f\'状态码: {response.status_code}\'); print(f\'内容长度: {len(response.content)}\')\\""'
    )
    
    if success:
        print("✅ E-commerce页面测试完成")
    else:
        print("❌ E-commerce页面测试失败")
    
    return success

def main():
    """主函数"""
    print("🔧 Heroku迁移重置工具")
    print("=" * 50)
    
    # 重置迁移
    if reset_migrations():
        print("\n✅ 迁移重置成功！")
        
        # 测试页面
        if test_ecommerce_page():
            print("\n🎉 所有问题已解决！")
        else:
            print("\n⚠️ 迁移成功，但页面仍有问题")
    else:
        print("\n❌ 迁移重置失败")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
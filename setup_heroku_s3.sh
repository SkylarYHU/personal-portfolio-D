#!/bin/bash

# AWS S3 Heroku配置脚本
# 使用方法: ./setup_heroku_s3.sh

echo "=== AWS S3 Heroku配置脚本 ==="
echo

# 检查是否安装了Heroku CLI
if ! command -v heroku &> /dev/null; then
    echo "错误: 请先安装Heroku CLI"
    echo "访问: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# 获取用户输入
read -p "请输入您的AWS Access Key ID: " AWS_ACCESS_KEY_ID
read -s -p "请输入您的AWS Secret Access Key: " AWS_SECRET_ACCESS_KEY
echo
read -p "请输入您的S3存储桶名称: " AWS_STORAGE_BUCKET_NAME
read -p "请输入AWS区域 (默认: us-east-1): " AWS_S3_REGION_NAME

# 设置默认区域
if [ -z "$AWS_S3_REGION_NAME" ]; then
    AWS_S3_REGION_NAME="us-east-1"
fi

echo
echo "正在配置Heroku环境变量..."

# 设置Heroku配置变量
heroku config:set AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" --app skylar-portfolio-2024
heroku config:set AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" --app skylar-portfolio-2024
heroku config:set AWS_STORAGE_BUCKET_NAME="$AWS_STORAGE_BUCKET_NAME" --app skylar-portfolio-2024
heroku config:set AWS_S3_REGION_NAME="$AWS_S3_REGION_NAME" --app skylar-portfolio-2024

echo
echo "✅ Heroku环境变量配置完成!"
echo
echo "接下来的步骤:"
echo "1. 运行: python manage.py upload_to_s3 (上传现有文件到S3)"
echo "2. 运行: git add . && git commit -m 'Add S3 configuration' && git push heroku main"
echo "3. 访问您的网站验证图片是否正常显示"
echo
echo "查看当前配置:"
heroku config --app skylar-portfolio-2024 | grep AWS
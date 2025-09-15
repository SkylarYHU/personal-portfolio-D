# AWS S3 配置指南

本指南将帮助您配置AWS S3来存储Django项目的媒体文件。

## 步骤1：创建S3存储桶

1. 登录AWS控制台：https://console.aws.amazon.com/
2. 搜索并进入"S3"服务
3. 点击"创建存储桶"
4. 配置存储桶：
   - **存储桶名称**：选择一个全球唯一的名称（例如：`your-portfolio-media-2024`）
   - **AWS区域**：选择离您用户最近的区域（推荐：`us-east-1`）
   - **阻止公共访问设置**：取消勾选"阻止所有公共访问"（因为需要公开访问图片）
   - 确认允许公共访问
5. 点击"创建存储桶"

## 步骤2：配置存储桶策略

1. 进入刚创建的存储桶
2. 点击"权限"选项卡
3. 在"存储桶策略"部分，点击"编辑"
4. 添加以下策略（替换`YOUR-BUCKET-NAME`为您的存储桶名称）：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
        }
    ]
}
```

## 步骤3：创建IAM用户

1. 在AWS控制台搜索"IAM"
2. 点击"用户" → "创建用户"
3. 用户名：`portfolio-s3-user`
4. 选择"直接附加策略"
5. 搜索并选择"AmazonS3FullAccess"策略
6. 创建用户
7. 进入用户详情页面，点击"安全证书"选项卡
8. 点击"创建访问密钥"
9. 选择"应用程序在AWS外部运行"
10. **重要**：保存访问密钥ID和秘密访问密钥

## 步骤4：配置环境变量

### 本地开发环境
创建`.env`文件（如果不存在）：
```bash
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

### Heroku生产环境
```bash
heroku config:set AWS_ACCESS_KEY_ID=your_access_key_id --app skylar-portfolio-2024
heroku config:set AWS_SECRET_ACCESS_KEY=your_secret_access_key --app skylar-portfolio-2024
heroku config:set AWS_STORAGE_BUCKET_NAME=your-bucket-name --app skylar-portfolio-2024
heroku config:set AWS_S3_REGION_NAME=us-east-1 --app skylar-portfolio-2024
```

## 步骤5：上传现有文件到S3

配置完环境变量后，运行以下命令上传现有的媒体文件：

```bash
python manage.py upload_to_s3
```

## 步骤6：部署到生产环境

```bash
git add .
git commit -m "Add AWS S3 configuration"
git push heroku main
```

## 验证配置

1. 检查S3存储桶中是否有上传的文件
2. 访问生产环境网站，确认图片正常显示
3. 图片URL应该类似：`https://your-bucket-name.s3.amazonaws.com/images/...`

## 费用说明

- **免费套餐**：5GB存储空间，20,000次GET请求，2,000次PUT请求/月
- **当前项目大小**：约179MB，完全在免费范围内
- **超出免费套餐后**：存储约$0.023/GB/月，请求费用很低

## 故障排除

1. **权限错误**：检查IAM用户权限和存储桶策略
2. **文件无法访问**：确认存储桶策略允许公共读取
3. **上传失败**：检查AWS凭证是否正确配置
4. **图片不显示**：检查MEDIA_URL配置和S3域名

## 安全建议

1. 定期轮换AWS访问密钥
2. 使用最小权限原则配置IAM策略
3. 启用S3访问日志记录
4. 考虑使用CloudFront CDN进一步优化性能
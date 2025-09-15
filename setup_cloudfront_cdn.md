# CloudFront CDN 配置指南

为了解决图片加载速度慢的问题，建议配置 AWS CloudFront CDN 来加速全球访问。

## 问题分析

当前配置存在以下性能问题：
1. **地理位置远**：S3存储桶位于 `eu-north-1`（斯德哥尔摩），对中国用户距离较远
2. **缺少CDN**：直接从S3加载，没有全球边缘节点缓存
3. **缓存策略**：已优化为1年缓存，但需要CDN分发

## 解决方案：配置 CloudFront CDN

### 步骤1：创建 CloudFront 分配

1. 登录 AWS 控制台，搜索 "CloudFront"
2. 点击 "创建分配"
3. 配置源域：
   - **源域**：`skylar-portfolio-media-2024.s3.eu-north-1.amazonaws.com`
   - **源路径**：留空
   - **名称**：`S3-skylar-portfolio-media`

### 步骤2：配置缓存行为

1. **查看器协议策略**：选择 "Redirect HTTP to HTTPS"
2. **允许的 HTTP 方法**：选择 "GET, HEAD"
3. **缓存策略**：选择 "Managed-CachingOptimized"
4. **源请求策略**：选择 "Managed-CORS-S3Origin"

### 步骤3：配置分配设置

1. **价格等级**：选择 "Use all edge locations (best performance)"
2. **备用域名 (CNAME)**：可选，如 `cdn.skylarhu.work`
3. **SSL 证书**：选择 "Default CloudFront Certificate"

### 步骤4：等待部署完成

- 部署通常需要 15-20 分钟
- 状态变为 "Deployed" 后即可使用
- 记录分配域名，格式如：`d1234567890123.cloudfront.net`

### 步骤5：配置环境变量

```bash
# 设置 CloudFront 域名
heroku config:set AWS_CLOUDFRONT_DOMAIN=d1234567890123.cloudfront.net --app skylarhu-portfolio
```

### 步骤6：部署更新

```bash
git add .
git commit -m "Add CloudFront CDN support for faster image loading"
git push heroku main
```

## 性能提升预期

配置 CloudFront 后，预期性能提升：
- **首次加载**：减少 50-70% 加载时间
- **重复访问**：减少 80-90% 加载时间（边缘缓存）
- **全球访问**：所有地区用户都能获得更快的加载速度

## 费用说明

- **免费套餐**：每月 1TB 数据传输，50万次请求
- **当前项目**：图片总大小约 179MB，完全在免费范围内
- **超出后费用**：数据传输约 $0.085/GB（中国地区）

## 验证配置

部署后检查：
1. 查看应用日志确认使用 CloudFront：`[SETTINGS] Using CloudFront CDN`
2. 检查图片URL是否指向 CloudFront 域名
3. 使用浏览器开发者工具测试加载速度
4. 检查响应头中的缓存设置

## 额外优化建议

1. **图片压缩**：使用 WebP 格式减少文件大小
2. **响应式图片**：根据设备提供不同尺寸
3. **懒加载**：实现图片懒加载减少初始加载时间
4. **预加载**：对关键图片使用 `<link rel="preload">`

## 故障排除

如果配置后仍然加载慢：
1. 检查 CloudFront 分配状态是否为 "Deployed"
2. 确认环境变量 `AWS_CLOUDFRONT_DOMAIN` 设置正确
3. 清除浏览器缓存重新测试
4. 检查 CloudFront 缓存命中率（AWS 控制台监控）
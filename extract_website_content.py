#!/usr/bin/env python
"""
网站内容提取脚本
提取 skylarhu.work 网站的所有文字信息，包括主页和详情页内容
"""

import os
import sys
import django
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from portfolioapp.models import (
    Project, BrandingProject, SocialMediaPost, 
    MobileLandingPage, EcommerceProject, PowerPointPresentation, Tag
)

def extract_all_content():
    """提取所有网站内容"""
    content = []
    
    # 添加时间戳
    content.append(f"# Skylar Hu Portfolio 网站内容备份")
    content.append(f"# 提取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    content.append(f"# 网站地址: https://skylarhu.work/")
    content.append("\n" + "="*80 + "\n")
    
    # 主页固定内容
    content.append("## 主页内容 (Home Page)\n")
    
    # 网站标题和描述
    content.append("### 网站标题")
    content.append("Skylar's Portfolio")
    content.append("\n### 网站描述")
    content.append("Skylar Hu's Portfolio - Dublin based developer showcasing projects in web development, digital marketing, and more.")
    
    # Hero Section
    content.append("\n### Hero Section")
    content.append("**主标题:** Graphic Designer")
    content.append("**描述:** I'm Skylar Hu, a graphic designer who bridges design, marketing, and development to craft cohesive brand experiences across digital and physical platforms.")
    
    # Table of Content
    content.append("\n### 目录 (Table of Content)")
    
    sections = [
        ("01", "Brand Design", "I create distinctive and professional brand identities that help businesses stand out and make a lasting impression."),
        ("02", "E-commerce Design", "I design user-friendly and conversion-focused e-commerce experiences that drive sales and enhance customer satisfaction through intuitive interfaces and seamless shopping flows."),
        ("03", "Social Media Design", "I craft engaging, on-brand graphics and templates that capture attention and keep your brand consistent across all platforms."),
        ("04", "Clinical Trial Presentation Design", "I create compelling and professional presentations that effectively communicate ideas, showcase projects, and engage audiences through clear visual storytelling."),
        ("05", "Mobile Landing Pages", "I build high-converting, fast, and visually compelling mobile landing pages that turn visitors into customers."),
        ("06", "Websites", "I design and develop user-friendly websites optimized for performance and built to showcase your brand effectively.")
    ]
    
    for num, title, desc in sections:
        content.append(f"**{num}. {title}**")
        content.append(f"{desc}")
        content.append("")
    
    # 工作经历
    content.append("\n### 工作经历 (Previous Role)")
    content.append("After time in China and New Zealand, my latest adventure has landed me in Dublin, where I'm focusing on the following challenges.")
    content.append("")
    
    roles = [
        ("Digital Marketing Specialist", "Zhihuiyuansi Network Technology Co.Ltd｜ 2021 - 2022", 
         "Designed and executed impactful advertising campaigns for Alibaba's mobile applications, significantly increasing user engagement and enhancing user experience through collaboration with cross-functional teams."),
        ("Advertising Operator", "Hangzhou Youshu Network Technology Co.Ltd ｜ 2020 - 2021",
         "Optimized advertising creatives and strategies to enhance overall ad performance, conducted A/B testing to identify the most effective campaigns, and continuously monitored performance to implement data-driven adjustments."),
        ("Junior Graphic Designer", "Shanghai Chuangji Advertising & Media | 2019 - 2020",
         "I have worked on creating packaging solutions such as shopping bags, food boxes, and wraps that strengthen brand recognition and enhance consumer engagement. In addition, I have developed brand identity systems—including logos and style guides—that ensure consistent visual communication across both digital and print platforms.")
    ]
    
    for title, company, desc in roles:
        content.append(f"**{title}**")
        content.append(f"{company}")
        content.append(f"{desc}")
        content.append("")
    
    # 客户经历
    content.append("\n### 客户经历 (Client Experience)")
    content.append("I've had the opportunity to collaborate with a diverse range of clients, including both emerging startups and well-established companies, such as:")
    content.append("")
    
    clients = ["Alibaba Group", "Goofish", "Fliggy", "Taobao", "Meituan", "Poizon", "Xiaohongshu", "Zhihu"]
    for client in clients:
        content.append(f"- {client}")
    
    # 联系信息
    content.append("\n### 联系信息 (Contact)")
    content.append("**标题:** Hit me up")
    content.append("**描述:** If you want to work with me or have any questions, feel free to email me.")
    content.append("**邮箱:** skylarhyn@gmail.com")
    content.append("**GitHub:** https://github.com/SkylarYHU")
    content.append("**LinkedIn:** https://www.linkedin.com/in/skylar-hu/")
    content.append("**技术说明:** Designed in Figma and developed in Visual Studio Code. Built with HTML, CSS and Python, deployed with Amazon Web Services. All components are carefully crafted to deliver a smooth user experience.")
    
    content.append("\n" + "="*80 + "\n")
    
    # 提取数据库内容
    extract_database_content(content)
    
    return "\n".join(content)

def extract_database_content(content):
    """提取数据库中的所有内容"""
    
    # 品牌设计项目
    content.append("## 品牌设计项目 (Brand Design Projects)\n")
    branding_projects = BrandingProject.objects.all().order_by('order')
    
    if branding_projects:
        for project in branding_projects:
            content.append(f"### {project.title}")
            content.append(f"**描述:** {project.description}")
            if project.about_brand:
                content.append(f"**关于品牌:** {project.about_brand}")
            if project.goals:
                content.append(f"**目标:** {project.goals}")
            if project.tools_apps:
                content.append(f"**工具和应用:** {project.tools_apps}")
            if project.tags.exists():
                tags = ", ".join([tag.name for tag in project.tags.all()])
                content.append(f"**标签:** {tags}")
            content.append("")
    else:
        content.append("暂无品牌设计项目数据")
        content.append("")
    
    # 电商设计项目
    content.append("\n## 电商设计项目 (E-commerce Design Projects)\n")
    ecommerce_projects = EcommerceProject.objects.all().order_by('order')
    
    if ecommerce_projects:
        for project in ecommerce_projects:
            content.append(f"### {project.title}")
            content.append(f"**描述:** {project.description}")
            if project.about_project:
                content.append(f"**关于项目:** {project.about_project}")
            if project.goals:
                content.append(f"**目标:** {project.goals}")
            if project.tools_apps:
                content.append(f"**工具和应用:** {project.tools_apps}")
            if project.tags.exists():
                tags = ", ".join([tag.name for tag in project.tags.all()])
                content.append(f"**标签:** {tags}")
            content.append("")
    else:
        content.append("暂无电商设计项目数据")
        content.append("")
    
    # 社交媒体设计
    content.append("\n## 社交媒体设计 (Social Media Design)\n")
    social_media_posts = SocialMediaPost.objects.all().order_by('order')
    
    if social_media_posts:
        for post in social_media_posts:
            content.append(f"### {post.title}")
            if post.category:
                content.append(f"**分类:** {post.category}")
            if post.about:
                content.append(f"**关于:** {post.about}")
            if post.goals:
                content.append(f"**目标:** {post.goals}")
            if post.tools:
                content.append(f"**工具:** {post.tools}")
            content.append("")
    else:
        content.append("暂无社交媒体设计数据")
        content.append("")
    
    # PowerPoint演示
    content.append("\n## PowerPoint演示 (PowerPoint Presentations)\n")
    presentations = PowerPointPresentation.objects.filter(is_active=True).order_by('order')
    
    if presentations:
        for presentation in presentations:
            content.append(f"### {presentation.title}")
            content.append(f"**关于内容:** {presentation.about_content}")
            content.append(f"**主要特性:** {presentation.key_features_content.replace('<br />', ', ')}")
            content.append(f"**目标受众:** {presentation.target_audience_content}")
            content.append(f"**工具和软件:** {presentation.tools_software_content}")
            if presentation.canvas_link_description:
                content.append(f"**Canvas链接描述:** {presentation.canvas_link_description}")
            if presentation.tags.exists():
                tags = ", ".join([tag.name for tag in presentation.tags.all()])
                content.append(f"**标签:** {tags}")
            content.append("")
    else:
        content.append("暂无PowerPoint演示数据")
        content.append("")
    
    # 移动端着陆页
    content.append("\n## 移动端着陆页 (Mobile Landing Pages)\n")
    mobile_pages = MobileLandingPage.objects.all().order_by('order')
    
    if mobile_pages:
        for page in mobile_pages:
            content.append(f"### {page.title}")
            content.append(f"**描述:** {page.description}")
            if page.about_brand:
                content.append(f"**关于品牌:** {page.about_brand}")
            if page.goals:
                content.append(f"**目标:** {page.goals}")
            if page.tools_apps:
                content.append(f"**工具和应用:** {page.tools_apps}")
            if page.tags.exists():
                tags = ", ".join([tag.name for tag in page.tags.all()])
                content.append(f"**标签:** {tags}")
            content.append("")
    else:
        content.append("暂无移动端着陆页数据")
        content.append("")
    
    # 网站项目
    content.append("\n## 网站项目 (Website Projects)\n")
    projects = Project.objects.all().order_by('order')
    
    if projects:
        for project in projects:
            content.append(f"### {project.title}")
            content.append(f"**描述:** {project.description}")
            if project.link:
                content.append(f"**链接:** {project.link}")
            if project.tags.exists():
                tags = ", ".join([tag.name for tag in project.tags.all()])
                content.append(f"**标签:** {tags}")
            content.append("")
    else:
        content.append("暂无网站项目数据")
        content.append("")
    
    # 所有标签
    content.append("\n## 所有标签 (All Tags)\n")
    all_tags = Tag.objects.all().order_by('name')
    
    if all_tags:
        tag_names = [tag.name for tag in all_tags]
        content.append(", ".join(tag_names))
    else:
        content.append("暂无标签数据")
    
    content.append("")

def main():
    """主函数"""
    try:
        print("开始提取网站内容...")
        
        # 提取所有内容
        all_content = extract_all_content()
        
        # 保存到文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"skylarhu_work_content_backup_{timestamp}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(all_content)
        
        print(f"✅ 内容提取完成！")
        print(f"📁 文件保存为: {filename}")
        print(f"📊 文件大小: {len(all_content)} 字符")
        
        # 显示统计信息
        print("\n📈 数据统计:")
        print(f"- 品牌设计项目: {BrandingProject.objects.count()} 个")
        print(f"- 电商设计项目: {EcommerceProject.objects.count()} 个")
        print(f"- 社交媒体设计: {SocialMediaPost.objects.count()} 个")
        print(f"- PowerPoint演示: {PowerPointPresentation.objects.filter(is_active=True).count()} 个")
        print(f"- 移动端着陆页: {MobileLandingPage.objects.count()} 个")
        print(f"- 网站项目: {Project.objects.count()} 个")
        print(f"- 标签总数: {Tag.objects.count()} 个")
        
    except Exception as e:
        print(f"❌ 提取过程中出现错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
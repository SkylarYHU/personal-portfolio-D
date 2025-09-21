from django.contrib import admin
from .models import Project, BrandingProject, Tag, SocialMediaPost, MobileLandingPage, EcommerceProject
from adminsortable2.admin import SortableAdminMixin


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # 显示项目标题和描述
    filter_horizontal = ('tags',)  # 允许在 admin 中选择标签
    ordering = ('order',)  # 默认根据 order 字段排序


@admin.register(BrandingProject)
class BrandingProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # 显示项目标题和描述
    filter_horizontal = ('tags',)  # 允许在 admin 中选择标签
    ordering = ('order',)  # 默认根据 order 字段排序
    
    # 添加字段分组，便于管理大量图片字段
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'description', 'image', 'link', 'order', 'tags')
        }),
        ('品牌详情', {
            'fields': ('about_brand', 'goals', 'tools_apps'),
            'classes': ('collapse',)
        }),
        ('品牌图片', {
            'fields': ('logos_image', 'typefaces_image', 'color_palette_image', 
                      'packaging_image', 'social_media_image', 'posters_banners_image', 'others_image'),
            'classes': ('collapse',)
        }),
    )
    
    # 添加保存时的错误处理提示
    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f'保存失败: {str(e)}。请检查图片文件大小是否超过10MB限制。')


@admin.register(SocialMediaPost)
class SocialMediaPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'about', 'tools', 'goals')
    ordering = ('order',)
    
    # 添加字段分组，便于管理图片和对应文本
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'order')
        }),
        ('拍立得相纸图片和文本', {
            'fields': ('mockup_image_1', 'mockup_image_1_text', 
                      'mockup_image_2', 'mockup_image_2_text',
                      'mockup_image_3', 'mockup_image_3_text'),
            'description': '为每个拍立得相纸图片设置对应的显示文本'
        }),
        ('详细信息', {
            'fields': ('about', 'tools', 'goals'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MobileLandingPage)
class MobileLandingPageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'description', 'link')
    ordering = ('order',)  # 默认根据 order 字段排序
    filter_horizontal = ('tags',)  # 允许在 admin 中选择标签
    
    # 添加字段分组，便于管理
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'description', 'image', 'link', 'order', 'tags')
        }),
        ('页面详情', {
            'fields': ('about_brand', 'goals'),
            'classes': ('collapse',)
        }),
        ('设计图片', {
            'fields': ('typefaces_image', 'color_palette_image', 'landing_pages_image'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EcommerceProject)
class EcommerceProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # 显示项目标题和描述
    filter_horizontal = ('tags',)  # 允许在 admin 中选择标签
    ordering = ('order',)  # 默认根据 order 字段排序
    
    # 添加字段分组，便于管理大量图片字段
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'description', 'image', 'link', 'order', 'tags')
        }),
        ('项目详情', {
            'fields': ('about_project', 'goals', 'tools_apps'),
            'classes': ('collapse',)
        }),
        ('设计图片', {
            'fields': ('design_process_image', 'user_interface_image', 'mobile_design_image', 
                      'product_pages_image', 'checkout_flow_image', 'others_image'),
            'classes': ('collapse',)
        }),
    )
    
    # 添加保存时的错误处理提示
    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f'保存失败: {str(e)}。请检查图片文件大小是否超过10MB限制。')


admin.site.register(Tag)

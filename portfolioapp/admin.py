from django.contrib import admin
from .models import Project, BrandingProject, Tag, SocialMediaPost, MobileLandingPage, EcommerceProject, PowerPointPresentation, MotionGraphicsProject
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
    list_display = ('title', 'category', 'date_posted', 'order')
    list_editable = ('order',)
    ordering = ('order',)
    # filter_horizontal = ('tags',)  # 临时禁用，生产环境缺少tags表
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'category', 'preview_image', 'order')
        }),
        ('项目内容', {
            'fields': ('about', 'goals', 'tools')
        }),
        ('项目图片', {
            'fields': ('image',)
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


@admin.register(PowerPointPresentation)
class PowerPointPresentationAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'date_posted')
    ordering = ('order',)
    list_filter = ('is_active', 'date_posted')
    filter_horizontal = ('tags',)  # 允许在 admin 中选择标签
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'powerpoint_link_url', 'order', 'is_active', 'tags')
        }),
        ('内容部分', {
            'fields': ('about_content', 'key_features_content', 'tools_software_content'),
            'classes': ('collapse',)
        }),
        ('Canvas 链接部分', {
            'fields': ('canvas_link_title', 'canvas_link_description', 'canvas_link_url', 'canvas_link_text'),
            'classes': ('collapse',)
        }),
        ('预览图片部分', {
            'fields': ('preview_title', 'preview_image', 'home_preview_image'),
            'classes': ('collapse',)
        }),
        ('附加信息', {
            'fields': ('target_audience_content',),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f'保存失败: {str(e)}。请检查图片文件大小是否超过10MB限制。')


@admin.register(MotionGraphicsProject)
class MotionGraphicsProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'date_posted', 'order')
    ordering = ('order',)
    list_filter = ('is_active', 'date_posted')
    filter_horizontal = ('tags',)
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'description', 'order', 'is_active', 'tags')
        }),
        ('视频文件', {
            'fields': ('video_file', 'video_url', 'preview_image'),
            'classes': ('collapse',)
        }),
        ('项目详情', {
            'fields': ('about_project', 'goals', 'tools_software'),
            'classes': ('collapse',)
        }),
        ('设计图片', {
            'fields': ('process_image', 'storyboard_image', 'final_output_image'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f'保存失败: {str(e)}。请检查文件大小是否超过限制。')


admin.site.register(Tag)

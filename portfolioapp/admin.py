from django.contrib import admin
from .models import Project, Tag
from adminsortable2.admin import SortableAdminMixin


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # 显示项目标题和描述
    filter_horizontal = ('tags',)  # 允许在 admin 中选择标签
    ordering = ('order',)  # 默认根据 order 字段排序


admin.site.register(Tag)

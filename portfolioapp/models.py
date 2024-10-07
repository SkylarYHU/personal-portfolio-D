from django.db import models

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    # blank=True 表示这个字段是可选的，可以为空。
    link = models.URLField(blank=True)
    # auto_now_add=True 表示每次创建一个新的 Project 实例时，自动将该字段设置为创建时的当前时间。
    date_posted = models.DateTimeField(auto_now_add=True, null=True)
    order = models.IntegerField(default=0)  # 添加顺序字段
    tags = models.ManyToManyField(Tag, blank=True)  # 添加标签字段，表示使用的技术

    class Meta:
        ordering = ['order']

    # __str__ 方法用于定义在打印 Project 对象时返回的内容。在这里，它返回项目的标题 self.title，方便在 Django 管理界面或 shell 中查看项目对象时能直观地显示项目名称。
    def __str__(self):
        return self.title

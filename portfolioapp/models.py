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


class BrandingProject(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to='images/branding/')
    link = models.URLField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)
    order = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    
    # Brand Design详情页面的可选部分
    about_brand = models.TextField(blank=True, help_text="About brand section content")
    goals = models.TextField(blank=True, help_text="Goals section content")
    tools_apps = models.TextField(blank=True, help_text="Tools & Apps section content")
    logos_image = models.ImageField(upload_to='images/branding/logos/', blank=True, help_text="Logos section image")
    typefaces_image = models.ImageField(upload_to='images/branding/typefaces/', blank=True, help_text="Typefaces section image")
    color_palette_image = models.ImageField(upload_to='images/branding/colors/', blank=True, help_text="Color palette section image")
    packaging_image = models.ImageField(upload_to='images/branding/packaging/', blank=True, help_text="Packaging section image")
    social_media_image = models.ImageField(upload_to='images/branding/social/', blank=True, help_text="Social media section image")
    posters_banners_image = models.ImageField(upload_to='images/branding/posters/', blank=True, help_text="Posters & banners section image")
    others_image = models.ImageField(upload_to='images/branding/others/', blank=True, help_text="Others section image")

    class Meta:
        ordering = ['order']
        verbose_name = 'Brand Design'
        verbose_name_plural = 'Brand Design'

    def __str__(self):
        return self.title


class SocialMediaPost(models.Model):
    title = models.CharField(max_length=128)  # 品类标题，如 "Food & Beverage"
    mockup_image_1 = models.ImageField(upload_to='images/social_media/')
    mockup_image_1_text = models.CharField(max_length=50, default='Design 01', help_text="拍立得相纸1的文本")
    mockup_image_2 = models.ImageField(upload_to='images/social_media/')
    mockup_image_2_text = models.CharField(max_length=50, default='Design 02', help_text="拍立得相纸2的文本")
    mockup_image_3 = models.ImageField(upload_to='images/social_media/')
    mockup_image_3_text = models.CharField(max_length=50, default='Design 03', help_text="拍立得相纸3的文本")
    about = models.TextField()  # About 部分的文字介绍
    tools = models.TextField()  # Tools & Apps 部分的文字介绍
    goals = models.TextField()  # Goals 部分的文字介绍
    date_posted = models.DateTimeField(auto_now_add=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Social Media Design'
        verbose_name_plural = 'Social Media Design'

    def __str__(self):
        return self.title


class MobileLandingPage(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to='images/mobile_landing/')
    link = models.URLField(max_length=200, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)
    order = models.IntegerField(default=0)
    
    # Mobile Landing Pages详情页面的可选部分
    about_brand = models.TextField(blank=True, help_text="About brand section content")
    goals = models.TextField(blank=True, help_text="Goals section content")
    typefaces_image = models.ImageField(upload_to='images/mobile_landing/typefaces/', blank=True, help_text="Typefaces section image")
    color_palette_image = models.ImageField(upload_to='images/mobile_landing/colors/', blank=True, help_text="Color palette section image")
    landing_pages_image = models.ImageField(upload_to='images/mobile_landing/pages/', blank=True, help_text="Landing Pages section image")

    class Meta:
        ordering = ['order']
        verbose_name = 'Mobile Landing Pages'
        verbose_name_plural = 'Mobile Landing Pages'

    def __str__(self):
        return self.title


class EcommerceProject(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to='images/ecommerce/')
    link = models.URLField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)
    order = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    
    # E-commerce Design详情页面的可选部分
    about_project = models.TextField(blank=True, help_text="About project section content")
    goals = models.TextField(blank=True, help_text="Goals section content")
    tools_apps = models.TextField(blank=True, help_text="Tools & Apps section content")
    design_process_image = models.ImageField(upload_to='images/ecommerce/process/', blank=True, help_text="Design process section image")
    user_interface_image = models.ImageField(upload_to='images/ecommerce/ui/', blank=True, help_text="User interface section image")
    mobile_design_image = models.ImageField(upload_to='images/ecommerce/mobile/', blank=True, help_text="Mobile design section image")
    product_pages_image = models.ImageField(upload_to='images/ecommerce/products/', blank=True, help_text="Product pages section image")
    checkout_flow_image = models.ImageField(upload_to='images/ecommerce/checkout/', blank=True, help_text="Checkout flow section image")
    others_image = models.ImageField(upload_to='images/ecommerce/others/', blank=True, help_text="Others section image")

    class Meta:
        ordering = ['order']
        verbose_name = 'E-commerce Design'
        verbose_name_plural = 'E-commerce Design'

    def __str__(self):
        return self.title

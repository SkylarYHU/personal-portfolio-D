from django.shortcuts import render, get_object_or_404
from .models import Project, BrandingProject, SocialMediaPost, MobileLandingPage, EcommerceProject, PowerPointPresentation

# Create your views here.


def home(request):
    projects = Project.objects.all()
    branding_projects = BrandingProject.objects.all()
    social_media_posts = SocialMediaPost.objects.all()
    mobile_landing_pages = MobileLandingPage.objects.all()
    ecommerce_projects = EcommerceProject.objects.all()
    powerpoint_presentations = PowerPointPresentation.objects.filter(is_active=True)
    return render(request, 'portfolioapp/home.html', {
        'projects': projects,
        'branding_projects': branding_projects,
        'social_media_posts': social_media_posts,
        'mobile_landing_pages': mobile_landing_pages,
        'ecommerce_projects': ecommerce_projects,
        'powerpoint_presentations': powerpoint_presentations
    })


def project_detail(request, project_id):
    # get_object_or_404 尝试根据给定的查询条件从数据库中获取对象。如果找到对象，则返回该对象；如果未找到，则会引发一个 Http404 异常，自动返回一个 404 页面，而不是抛出错误。
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'portfolioapp/project_detail.html', {"project": project})


def branding_detail(request, branding_id):
    branding_project = get_object_or_404(BrandingProject, id=branding_id)
    return render(request, 'portfolioapp/branding_detail.html', {"branding_project": branding_project})


def mobile_landing_page_detail(request, mobile_landing_page_id):
    mobile_landing_page = get_object_or_404(
        MobileLandingPage, id=mobile_landing_page_id)
    return render(request, 'portfolioapp/mobile_landing_page_detail.html', {"mobile_landing_page": mobile_landing_page})


def ecommerce_detail(request, ecommerce_id):
    ecommerce_project = get_object_or_404(EcommerceProject, id=ecommerce_id)
    return render(request, 'portfolioapp/ecommerce_detail.html', {"ecommerce_project": ecommerce_project})


def powerpoint_detail(request):
    # 获取第一个激活的 PowerPoint 演示文稿，如果没有则创建默认的
    try:
        presentation = PowerPointPresentation.objects.filter(is_active=True).first()
        if not presentation:
            # 如果没有激活的演示文稿，创建一个默认的
            presentation = PowerPointPresentation.objects.create()
    except PowerPointPresentation.DoesNotExist:
        # 如果表不存在或没有数据，创建一个默认的
        presentation = PowerPointPresentation.objects.create()
    
    return render(request, 'portfolioapp/powerpoint_detail.html', {'presentation': presentation})

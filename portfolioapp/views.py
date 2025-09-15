from django.shortcuts import render, get_object_or_404
from .models import Project, BrandingProject, SocialMediaPost, MobileLandingPage

# Create your views here.


def home(request):
    projects = Project.objects.all()
    branding_projects = BrandingProject.objects.all()
    social_media_posts = SocialMediaPost.objects.all()
    mobile_landing_pages = MobileLandingPage.objects.all()
    return render(request, 'portfolioapp/home.html', {
        'projects': projects,
        'branding_projects': branding_projects,
        'social_media_posts': social_media_posts,
        'mobile_landing_pages': mobile_landing_pages
    })


def project_detail(request, project_id):
    # get_object_or_404 尝试根据给定的查询条件从数据库中获取对象。如果找到对象，则返回该对象；如果未找到，则会引发一个 Http404 异常，自动返回一个 404 页面，而不是抛出错误。
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'portfolioapp/project_detail.html', {"project": project})


def branding_detail(request, branding_id):
    branding_project = get_object_or_404(BrandingProject, id=branding_id)
    return render(request, 'portfolioapp/branding_detail.html', {"branding_project": branding_project})


def mobile_landing_page_detail(request, mobile_landing_page_id):
    mobile_landing_page = get_object_or_404(MobileLandingPage, id=mobile_landing_page_id)
    return render(request, 'portfolioapp/mobile_landing_page_detail.html', {"mobile_landing_page": mobile_landing_page})

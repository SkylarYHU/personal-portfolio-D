from django.shortcuts import render, get_object_or_404
from .models import Project

# Create your views here.


def home(request):
    projects = Project.objects.all()
    return render(request, 'portfolioapp/home.html', {"projects": projects})


def project_detail(request, project_id):
    # get_object_or_404 尝试根据给定的查询条件从数据库中获取对象。如果找到对象，则返回该对象；如果未找到，则会引发一个 Http404 异常，自动返回一个 404 页面，而不是抛出错误。
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'portfolioapp/project_detail.html', {"project": project})

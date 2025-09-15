from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('project/<int:project_id>', views.project_detail, name="project_detail"),
    path('branding/<int:branding_id>', views.branding_detail, name="branding_detail"),
    path('mobile-landing-page/<int:mobile_landing_page_id>', views.mobile_landing_page_detail, name="mobile_landing_page_detail")
]

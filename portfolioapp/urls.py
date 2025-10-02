from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('project/<int:project_id>', views.project_detail, name="project_detail"),
    path('branding/<int:branding_id>',
         views.branding_detail, name="branding_detail"),
    path('mobile-landing-page/<int:mobile_landing_page_id>',
         views.mobile_landing_page_detail, name="mobile_landing_page_detail"),
    path('ecommerce/<int:ecommerce_id>',
         views.ecommerce_detail, name="ecommerce_detail"),
    path('powerpoint/', views.powerpoint_detail, name="powerpoint_detail"),
    path('social-media/<int:social_media_id>',
         views.social_media_detail, name="social_media_detail"),
    path('motion-graphics/<int:motion_graphics_id>',
         views.motion_graphics_detail, name="motion_graphics_detail")
]

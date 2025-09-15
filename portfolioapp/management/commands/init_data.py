from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portfolioapp.models import Project, Tag, BrandingProject, SocialMediaPost, MobileLandingPage

class Command(BaseCommand):
    help = 'Initialize sample data for the portfolio'

    def handle(self, *args, **options):
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superuser created'))

        # Create tags
        tag1, _ = Tag.objects.get_or_create(name='Branding')
        tag2, _ = Tag.objects.get_or_create(name='Web Design')
        tag3, _ = Tag.objects.get_or_create(name='Mobile')

        # Create branding projects
        if not BrandingProject.objects.exists():
            branding1 = BrandingProject.objects.create(
                title='Alibaba Brand Identity',
                description='Complete brand identity design for Alibaba including logo, color palette, and brand guidelines.',
                image='static/images/Alibaba-logo.png',
                about_brand='Alibaba is a leading e-commerce platform.',
                brand_logo='static/images/Alibaba-logo.svg',
                brand_color_palette='#FF6A00, #FFFFFF, #000000'
            )
            
            branding2 = BrandingProject.objects.create(
                title='Meituan Brand Design',
                description='Brand redesign project for Meituan food delivery platform.',
                image='static/images/meituan-logo.png',
                about_brand='Meituan is China\'s leading food delivery service.',
                brand_logo='static/images/meituan-logo.svg',
                brand_color_palette='#FFD100, #32CD32, #FFFFFF'
            )
            
            branding3 = BrandingProject.objects.create(
                title='Taobao Visual Identity',
                description='Visual identity system for Taobao marketplace.',
                image='static/images/taobao-logo.png',
                about_brand='Taobao is China\'s largest online shopping platform.',
                brand_logo='static/images/taobao-logo1.svg',
                brand_color_palette='#FF4500, #FFA500, #FFFFFF'
            )
            
            self.stdout.write(self.style.SUCCESS('Branding projects created'))

        # Create sample projects
        if not Project.objects.exists():
            project1 = Project.objects.create(
                title='Sample Project 1',
                description='This is a sample project description.',
                image='projects/sample1.jpg'
            )
            project1.tags.add(tag1, tag2)
            
            project2 = Project.objects.create(
                title='Sample Project 2', 
                description='Another sample project description.',
                image='projects/sample2.jpg'
            )
            project2.tags.add(tag2, tag3)
            
            self.stdout.write(self.style.SUCCESS('Sample projects created'))

        self.stdout.write(self.style.SUCCESS('Data initialization completed!'))
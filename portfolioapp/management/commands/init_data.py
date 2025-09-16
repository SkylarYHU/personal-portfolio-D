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
                image='images/Alibaba-logo.svg',
                about_brand='Alibaba is a leading e-commerce platform.',
                goals='Create a modern and trustworthy brand identity for the e-commerce platform.',
                tools_apps='Adobe Illustrator, Adobe Photoshop, Figma'
            )
            
            branding2 = BrandingProject.objects.create(
                title='Meituan Brand Design',
                description='Brand redesign project for Meituan food delivery platform.',
                image='images/meituan-logo.svg',
                about_brand='Meituan is China\'s leading food delivery service.',
                goals='Redesign the brand to be more modern and user-friendly.',
                tools_apps='Adobe Creative Suite, Sketch'
            )
            
            branding3 = BrandingProject.objects.create(
                title='Taobao Visual Identity',
                description='Visual identity system for Taobao marketplace.',
                image='images/taobao-logo1.svg',
                about_brand='Taobao is China\'s largest online shopping platform.',
                goals='Create a cohesive visual identity system for the marketplace.',
                tools_apps='Adobe Illustrator, Adobe Photoshop'
            )
            
            self.stdout.write(self.style.SUCCESS('Branding projects created'))

        # Create sample projects
        if not Project.objects.exists():
            project1 = Project.objects.create(
                title='Sample Project 1',
                description='This is a sample project description.',
                image='images/home.png'
            )
            project1.tags.add(tag1, tag2)
            
            project2 = Project.objects.create(
                title='Sample Project 2', 
                description='Another sample project description.',
                image='images/cube.png'
            )
            project2.tags.add(tag2, tag3)
            
            self.stdout.write(self.style.SUCCESS('Sample projects created'))

        # Create social media posts
        if not SocialMediaPost.objects.exists():
            social1 = SocialMediaPost.objects.create(
                title='Food & Beverage',
                mockup_image_1='images/meituan-logo.svg',
                mockup_image_2='images/taobao-logo1.svg',
                mockup_image_3='images/Alibaba-logo.svg',
                about='Creative social media designs for food and beverage brands.',
                tools='Adobe Photoshop, Illustrator, Figma',
                goals='Increase brand engagement and visual appeal.'
            )
            
            self.stdout.write(self.style.SUCCESS('Social media posts created'))

        # Create mobile landing pages
        if not MobileLandingPage.objects.exists():
            mobile1 = MobileLandingPage.objects.create(
                title='E-commerce App Landing',
                description='Modern mobile landing page design for e-commerce applications.',
                image='images/sphere.png',
                about_brand='Innovative mobile experience design.',
                goals='Create intuitive and engaging mobile interfaces.'
            )
            mobile1.tags.add(tag3)
            
            self.stdout.write(self.style.SUCCESS('Mobile landing pages created'))

        self.stdout.write(self.style.SUCCESS('Data initialization completed!'))
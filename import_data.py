#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from django.contrib.auth.models import User
from portfolioapp.models import Project, Tag, BrandingProject, SocialMediaPost, MobileLandingPage

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created')

# Create some sample data
# Create tags
tag1, _ = Tag.objects.get_or_create(name='Branding')
tag2, _ = Tag.objects.get_or_create(name='Web Design')
tag3, _ = Tag.objects.get_or_create(name='Mobile')

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
    
    print('Sample projects created')

print('Data import completed!')
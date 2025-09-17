#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from portfolioapp.models import SocialMediaPost

# Check SocialMediaPost data
posts = SocialMediaPost.objects.all()
print(f"Total SocialMediaPost records: {posts.count()}")
print("=" * 60)

for i, post in enumerate(posts, 1):
    print(f"Post {i}: {post.title}")
    print(f"About field: {'✓ Has content' if post.about and post.about.strip() else '✗ Empty or None'}")
    if post.about and post.about.strip():
        print(f"About content (first 100 chars): {post.about[:100]}...")
    
    print(f"Goals field: {'✓ Has content' if post.goals and post.goals.strip() else '✗ Empty or None'}")
    if post.goals and post.goals.strip():
        print(f"Goals content (first 100 chars): {post.goals[:100]}...")
    
    print(f"Tools field: {'✓ Has content' if post.tools and post.tools.strip() else '✗ Empty or None'}")
    if post.tools and post.tools.strip():
        print(f"Tools content (first 100 chars): {post.tools[:100]}...")
    
    print("-" * 60)

print("\nDone checking SocialMediaPost data.")
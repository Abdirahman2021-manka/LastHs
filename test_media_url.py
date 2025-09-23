#!/usr/bin/env python
"""
Quick test to verify media URLs are working.
Run this and then test the URLs in your browser.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habiba_blog.settings')
django.setup()

from blog.models import BlogPost
from django.conf import settings

def main():
    print("🌐 Media URL Test")
    print("=" * 40)
    print(f"DEBUG Mode: {settings.DEBUG}")
    print(f"Media URL: {settings.MEDIA_URL}")
    print()
    
    # Get posts with images
    posts = BlogPost.objects.filter(featured_image__isnull=False).exclude(featured_image='')
    
    if not posts.exists():
        print("❌ No blog posts with images found")
        return
    
    print("📝 Blog posts with images:")
    print("-" * 30)
    
    for post in posts:
        print(f"Title: {post.title}")
        print(f"Image: {post.featured_image.name}")
        print(f"URL: {post.featured_image.url}")
        print(f"Full URL: http://localhost:8000{post.featured_image.url}")
        print()
    
    print("🧪 Testing Instructions:")
    print("1. Start your Django server: python manage.py runserver")
    print("2. Open the URLs above in your browser")
    print("3. If images load, the issue is fixed!")
    print("4. If images don't load, check the server console for errors")

if __name__ == "__main__":
    main()
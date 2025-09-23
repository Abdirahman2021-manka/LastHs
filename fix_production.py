#!/usr/bin/env python
"""
Script to fix production deployment issues.
Run this to collect static files and check your deployment.
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

from django.core.management import call_command
from django.conf import settings

def main():
    print("🔧 Fixing Production Deployment Issues")
    print("=" * 50)
    
    # Check current settings
    print(f"DEBUG Mode: {settings.DEBUG}")
    print(f"Static Root: {settings.STATIC_ROOT}")
    print(f"Media Root: {settings.MEDIA_ROOT}")
    print()
    
    # Collect static files
    print("📦 Collecting static files...")
    try:
        call_command('collectstatic', '--noinput', '--clear')
        print("✅ Static files collected successfully")
    except Exception as e:
        print(f"❌ Error collecting static files: {e}")
    
    print()
    
    # Check if required files exist
    static_root = Path(settings.STATIC_ROOT)
    required_files = [
        'css/output.css',
        'img/hasil.png',
    ]
    
    print("🔍 Checking required files:")
    for file_path in required_files:
        full_path = static_root / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
    
    print()
    
    # Check media files
    print("🖼️  Checking media files:")
    from blog.models import BlogPost
    posts_with_images = BlogPost.objects.filter(featured_image__isnull=False).exclude(featured_image='')
    
    for post in posts_with_images:
        image_path = Path(settings.MEDIA_ROOT) / post.featured_image.name
        if image_path.exists():
            print(f"✅ {post.featured_image.name}")
        else:
            print(f"❌ {post.featured_image.name} - MISSING")
    
    print()
    print("🎯 Summary:")
    print("1. Static files have been collected")
    print("2. Check the missing files above")
    print("3. Upload missing media files to your server")
    print("4. Restart your application")
    print()
    print("💡 For Railway deployment:")
    print("- Make sure your DATABASE_URL is set correctly")
    print("- Upload media files to your server")
    print("- Check your build process includes static file collection")

if __name__ == "__main__":
    main()

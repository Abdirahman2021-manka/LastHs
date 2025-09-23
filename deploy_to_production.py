#!/usr/bin/env python
"""
Script to prepare and deploy fixes to production server.
This will help you update your Railway deployment with the image fixes.
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
    print("🚀 Preparing Production Deployment")
    print("=" * 50)
    
    # Check current settings
    print(f"DEBUG Mode: {settings.DEBUG}")
    print(f"Static Root: {settings.STATIC_ROOT}")
    print(f"Media Root: {settings.MEDIA_ROOT}")
    print()
    
    # Collect static files for production
    print("📦 Collecting static files for production...")
    try:
        call_command('collectstatic', '--noinput', '--clear')
        print("✅ Static files collected successfully")
    except Exception as e:
        print(f"❌ Error collecting static files: {e}")
        return
    
    print()
    
    # Check if required files exist
    static_root = Path(settings.STATIC_ROOT)
    required_files = [
        'css/output.css',
        'img/hasil.png',
    ]
    
    print("🔍 Checking required static files:")
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
    print("🎯 Production Deployment Steps:")
    print("=" * 50)
    print("1. 📁 Commit all changes to Git:")
    print("   git add .")
    print("   git commit -m 'Fix image display issues'")
    print()
    print("2. 🚀 Push to Railway:")
    print("   git push origin main")
    print()
    print("3. 🔧 On Railway, run these commands:")
    print("   python manage.py collectstatic --noinput")
    print("   python manage.py migrate")
    print()
    print("4. 📤 Upload media files to Railway:")
    print("   - Go to Railway dashboard")
    print("   - Upload your media files to the /media directory")
    print("   - Or use Railway CLI to upload files")
    print()
    print("5. 🔄 Restart your Railway service")
    print()
    print("💡 Alternative: Use Railway CLI to deploy:")
    print("   railway login")
    print("   railway link")
    print("   railway up")
    print()
    print("✅ After deployment, your images should work correctly!")

if __name__ == "__main__":
    main()

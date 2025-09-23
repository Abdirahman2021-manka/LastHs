#!/usr/bin/env python
"""
Test script to verify media file serving is working correctly.
Run this script to check if your media files are accessible.
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

from django.conf import settings
from blog.models import BlogPost
from django.core.files.storage import default_storage

def test_media_files():
    """Test if media files are accessible and properly configured."""
    print("🔍 Testing Media File Configuration")
    print("=" * 50)
    
    # Check settings
    print(f"📁 MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"🌐 MEDIA_URL: {settings.MEDIA_URL}")
    print(f"🐛 DEBUG: {settings.DEBUG}")
    print()
    
    # Check if media directory exists
    media_root = Path(settings.MEDIA_ROOT)
    if media_root.exists():
        print(f"✅ Media directory exists: {media_root}")
    else:
        print(f"❌ Media directory does not exist: {media_root}")
        return
    
    # Check blog posts with images
    posts_with_images = BlogPost.objects.filter(featured_image__isnull=False).exclude(featured_image='')
    print(f"📝 Found {posts_with_images.count()} blog posts with featured images")
    print()
    
    for post in posts_with_images[:5]:  # Check first 5 posts
        print(f"📄 Post: {post.title}")
        print(f"   Image field: {post.featured_image}")
        
        if post.featured_image:
            # Check if file exists on disk
            file_path = media_root / post.featured_image.name
            if file_path.exists():
                print(f"   ✅ File exists on disk: {file_path}")
                print(f"   📏 File size: {file_path.stat().st_size} bytes")
                
                # Test URL generation
                try:
                    url = post.featured_image.url
                    print(f"   🌐 Generated URL: {url}")
                except Exception as e:
                    print(f"   ❌ URL generation failed: {e}")
            else:
                print(f"   ❌ File missing on disk: {file_path}")
        print()
    
    # Test media serving
    print("🧪 Testing Media Serving")
    print("-" * 30)
    
    if posts_with_images.exists():
        test_post = posts_with_images.first()
        if test_post.featured_image:
            try:
                # Test if we can read the file
                with open(media_root / test_post.featured_image.name, 'rb') as f:
                    content = f.read(1024)  # Read first 1KB
                print(f"✅ Can read file: {len(content)} bytes read")
                
                # Test URL construction
                expected_url = f"{settings.MEDIA_URL}{test_post.featured_image.name}"
                print(f"🔗 Expected URL: {expected_url}")
                
            except Exception as e:
                print(f"❌ Error reading file: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Media file test completed!")
    print("\nIf you see any ❌ errors above, those are the issues to fix.")
    print("If all tests pass, your media files should be working correctly.")

if __name__ == "__main__":
    test_media_files()

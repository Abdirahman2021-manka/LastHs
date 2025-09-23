#!/usr/bin/env python
import requests
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habiba_blog.settings')
django.setup()

from blog.models import BlogPost

# Get a post with an image
post = BlogPost.objects.filter(featured_image__isnull=False).first()
if post:
    image_url = f"http://localhost:8000{post.featured_image.url}"
    print(f"Testing URL: {image_url}")
    
    try:
        response = requests.get(image_url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'Unknown')}")
        print(f"Content Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("✅ Media file is accessible!")
        else:
            print("❌ Media file is not accessible")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error accessing media file: {e}")
else:
    print("No posts with images found")

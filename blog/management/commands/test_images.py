from django.core.management.base import BaseCommand
from django.conf import settings
from blog.models import BlogPost
import os
from django.test import Client


class Command(BaseCommand):
    help = 'Test blog post image URLs and media serving'

    def handle(self, *args, **options):
        self.stdout.write("=== Blog Image Testing Utility ===")
        
        # Check settings
        self.stdout.write(f"DEBUG: {settings.DEBUG}")
        self.stdout.write(f"MEDIA_URL: {settings.MEDIA_URL}")
        self.stdout.write(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
        self.stdout.write()
        
        # Check blog posts with images
        posts = BlogPost.objects.filter(featured_image__isnull=False)
        self.stdout.write(f"Found {posts.count()} posts with featured images:")
        self.stdout.write()
        
        for post in posts:
            self.stdout.write(f"Post: {post.title}")
            self.stdout.write(f"Image: {post.featured_image}")
            self.stdout.write(f"URL: {post.featured_image.url}")
            
            # Check if file exists
            if os.path.exists(post.featured_image.path):
                self.stdout.write(self.style.SUCCESS("✅ File exists on disk"))
            else:
                self.stdout.write(self.style.ERROR("❌ File missing from disk"))
            
            # Test URL accessibility (if server is running)
            try:
                client = Client()
                response = client.get(post.featured_image.url)
                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS("✅ URL accessible via Django"))
                else:
                    self.stdout.write(self.style.ERROR(f"❌ URL not accessible: {response.status_code}"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⚠️  Could not test URL: {e}"))
            
            self.stdout.write("-" * 50)
        
        # Instructions
        self.stdout.write()
        self.stdout.write("=== Instructions ===")
        if not settings.DEBUG:
            self.stdout.write(self.style.WARNING("⚠️  DEBUG is False - media files won't be served"))
            self.stdout.write("To fix: Start server with DEBUG=True")
            self.stdout.write("Windows: $env:DEBUG='True'; python manage.py runserver")
            self.stdout.write("Linux/Mac: DEBUG=True python manage.py runserver")
        else:
            self.stdout.write(self.style.SUCCESS("✅ DEBUG is True - media files should be served"))
            self.stdout.write("Access your site at: http://localhost:8000")
        
        self.stdout.write()
        self.stdout.write("If images still don't work:")
        self.stdout.write("1. Make sure Django server is running")
        self.stdout.write("2. Access site through Django server (not static files)")
        self.stdout.write("3. Check browser developer tools for 404 errors")

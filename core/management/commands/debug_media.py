from django.core.management.base import BaseCommand
from django.conf import settings
from django.urls import reverse
from blog.models import BlogPost
from django.test import RequestFactory
from core.media_views import serve_media

class Command(BaseCommand):
    help = 'Debug media file serving issues'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Debugging Media File Serving")
        self.stdout.write("=" * 50)
        
        # Check settings
        self.stdout.write(f"DEBUG: {settings.DEBUG}")
        self.stdout.write(f"MEDIA_URL: {settings.MEDIA_URL}")
        self.stdout.write(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
        self.stdout.write("")
        
        # Test with a real blog post
        posts = BlogPost.objects.filter(featured_image__isnull=False).exclude(featured_image='')
        if not posts.exists():
            self.stdout.write("❌ No blog posts with images found")
            return
            
        post = posts.first()
        self.stdout.write(f"Testing with post: {post.title}")
        self.stdout.write(f"Image: {post.featured_image}")
        self.stdout.write(f"Image URL: {post.featured_image.url}")
        self.stdout.write("")
        
        # Test the media serving view directly
        factory = RequestFactory()
        request = factory.get(post.featured_image.url)
        
        try:
            response = serve_media(request, post.featured_image.name)
            self.stdout.write(f"✅ Media view response: {response.status_code}")
            self.stdout.write(f"Content-Type: {response.get('Content-Type', 'Not set')}")
            self.stdout.write(f"Content-Length: {response.get('Content-Length', 'Not set')}")
        except Exception as e:
            self.stdout.write(f"❌ Media view error: {e}")
        
        self.stdout.write("")
        self.stdout.write("🌐 Test URLs:")
        self.stdout.write(f"Direct file: {post.featured_image.url}")
        self.stdout.write(f"Full URL: http://localhost:8000{post.featured_image.url}")
        self.stdout.write("")
        self.stdout.write("💡 If images are still broken, check:")
        self.stdout.write("1. Make sure you're running the development server: python manage.py runserver")
        self.stdout.write("2. Check if DEBUG=True in settings")
        self.stdout.write("3. Verify the media URL is accessible in your browser")

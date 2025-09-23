from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command
import os
from pathlib import Path

class Command(BaseCommand):
    help = 'Check and prepare for production deployment'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Production Deployment Check")
        self.stdout.write("=" * 50)
        
        # Check DEBUG mode
        if settings.DEBUG:
            self.stdout.write("⚠️  WARNING: DEBUG is True - this should be False in production")
        else:
            self.stdout.write("✅ DEBUG is False - good for production")
        
        # Check static files
        static_root = Path(settings.STATIC_ROOT)
        if static_root.exists():
            self.stdout.write(f"✅ Static files directory exists: {static_root}")
        else:
            self.stdout.write(f"❌ Static files directory missing: {static_root}")
            self.stdout.write("   Run: python manage.py collectstatic --noinput")
        
        # Check media files
        media_root = Path(settings.MEDIA_ROOT)
        if media_root.exists():
            self.stdout.write(f"✅ Media files directory exists: {media_root}")
        else:
            self.stdout.write(f"❌ Media files directory missing: {media_root}")
        
        # Check database
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write("✅ Database connection working")
        except Exception as e:
            self.stdout.write(f"❌ Database connection failed: {e}")
        
        # Check required files
        required_files = [
            'static/css/output.css',
            'static/img/hasil.png',
        ]
        
        for file_path in required_files:
            full_path = static_root / file_path
            if full_path.exists():
                self.stdout.write(f"✅ {file_path} exists")
            else:
                self.stdout.write(f"❌ {file_path} missing")
        
        # Check media files
        from blog.models import BlogPost
        posts_with_images = BlogPost.objects.filter(featured_image__isnull=False).exclude(featured_image='')
        self.stdout.write(f"📝 Found {posts_with_images.count()} blog posts with images")
        
        for post in posts_with_images:
            image_path = media_root / post.featured_image.name
            if image_path.exists():
                self.stdout.write(f"✅ {post.featured_image.name} exists")
            else:
                self.stdout.write(f"❌ {post.featured_image.name} missing")
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("💡 Next steps:")
        self.stdout.write("1. Run: python manage.py collectstatic --noinput")
        self.stdout.write("2. Check your DATABASE_URL environment variable")
        self.stdout.write("3. Ensure all media files are uploaded")
        self.stdout.write("4. Restart your server")

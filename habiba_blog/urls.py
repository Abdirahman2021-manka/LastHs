from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from core.media_views import serve_media

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Homepage and main pages
    path('blog/', include('blog.urls')),  # Blog functionality
    path('users/', include('users.urls')),  # Authentication (includes logout)
    path('newsletter/', include('newsletter.urls')),  # Newsletter
    path('analytics/', include('analytics.urls')),  # Analytics (optional)
    path('ckeditor/', include('ckeditor_uploader.urls')),  # CKEditor uploads
]

# Serve static and media files
if settings.DEBUG:
    # Development mode - use Django's built-in serving
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Production mode - use custom media serving view
    urlpatterns += [
        path('media/<path:path>', serve_media, name='media'),
    ]
    # Static files should be served by web server in production
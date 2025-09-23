from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

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
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Additional media serving for production (when DEBUG=False)
if not settings.DEBUG:
    from django.views.static import serve
    from django.urls import re_path
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
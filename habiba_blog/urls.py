from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),        # Homepage and main pages
    path('blog/', include('blog.urls')),   # Blog functionality
    path('users/', include('users.urls')), # Authentication
    path('newsletter/', include('newsletter.urls')), # Newsletter
    path('analytics/', include('analytics.urls')),   # Analytics
    path('ckeditor/', include('ckeditor_uploader.urls')),  # CKEditor uploads
]

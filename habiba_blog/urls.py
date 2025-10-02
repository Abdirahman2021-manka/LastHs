from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def health_check(request):
    """Simple health check endpoint for Railway"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Django application is running'
    })

urlpatterns = [
    path('health/', csrf_exempt(health_check), name='health_check'),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),        # Homepage and main pages
    path('blog/', include('blog.urls')),   # Blog functionality
    path('users/', include('users.urls')), # Authentication
    path('newsletter/', include('newsletter.urls')), # Newsletter
    path('analytics/', include('analytics.urls')),   # Analytics
    path('ckeditor/', include('ckeditor_uploader.urls')),  # CKEditor uploads
]

from django.http import HttpResponse, Http404, HttpResponseNotModified
from django.conf import settings
from django.utils.http import http_date
from django.views.static import was_modified_since
import os
import mimetypes

def serve_media(request, path):
    """Custom view to serve media files in production"""
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    # Security check - ensure the path is within MEDIA_ROOT
    if not str(file_path).startswith(str(settings.MEDIA_ROOT)):
        raise Http404("Invalid file path")
    
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise Http404("File not found")
    
    try:
        # Check if file was modified since last request
        stat = os.stat(file_path)
        if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'), stat.st_mtime):
            return HttpResponseNotModified()
        
        # Determine content type
        content_type, encoding = mimetypes.guess_type(file_path)
        if content_type is None:
            content_type = 'application/octet-stream'
        
        # Read file content
        with open(file_path, 'rb') as f:
            content = f.read()
        
        response = HttpResponse(content, content_type=content_type)
        response['Content-Length'] = len(content)
        response['Last-Modified'] = http_date(stat.st_mtime)
        
        # Set cache headers for better performance
        response['Cache-Control'] = 'public, max-age=31536000'  # 1 year
        response['Expires'] = http_date(stat.st_mtime + 31536000)
        
        return response
        
    except (IOError, OSError) as e:
        raise Http404("Error serving file")

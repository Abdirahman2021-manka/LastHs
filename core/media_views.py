from django.http import HttpResponse, Http404
from django.conf import settings
import os

def serve_media(request, path):
    """Custom view to serve media files in production"""
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    if not os.path.exists(file_path):
        raise Http404("File not found")
    
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Determine content type based on file extension
        if file_path.lower().endswith(('.jpg', '.jpeg')):
            content_type = 'image/jpeg'
        elif file_path.lower().endswith('.png'):
            content_type = 'image/png'
        elif file_path.lower().endswith('.gif'):
            content_type = 'image/gif'
        elif file_path.lower().endswith('.webp'):
            content_type = 'image/webp'
        else:
            content_type = 'application/octet-stream'
        
        response = HttpResponse(content, content_type=content_type)
        response['Content-Length'] = len(content)
        return response
        
    except Exception as e:
        raise Http404("Error serving file")

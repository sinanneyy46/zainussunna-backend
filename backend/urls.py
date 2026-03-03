"""
URL Configuration for Backend
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request):
    """API root - list available endpoints"""
    return Response({
        'message': 'Zainussunna Academy API',
        'version': '1.0.0',
        'endpoints': {
            'programs': '/api/programs/',
            'admissions': '/api/admissions/',
            'content': '/api/content/',
            'achievements': '/api/achievements/',
            'gallery': '/api/gallery/',
            'enquiries': '/api/enquiries/',
            'analytics': '/api/analytics/',
            'auth': '/api/auth/',
            'health': '/api/health/',
        },
        'documentation': '/api/docs/',
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root),
    path('api/core/', include('core.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


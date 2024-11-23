import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Attendify DRF API",
        default_version='v1',
        description="API for Attendify DRF",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@araltech.local"),
        license=openapi.License(name="BSD License"),
    ),
    # url=os.getenv('API_SCHEMA_URL', 'http://localhost:8000'),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('employees/', include('employees.urls')),
    path('clients/', include('clients.urls')),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += [
        # API schema
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
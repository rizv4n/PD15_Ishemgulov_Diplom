from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from core import urls as core_urls
from social_django import urls as social_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include(core_urls)),
    path('oauth/', include(social_urls, namespace='social')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema')),
]

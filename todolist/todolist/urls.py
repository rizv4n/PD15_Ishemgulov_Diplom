from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from bot.views import BotVerifyView
from core import urls as core_urls
from goals import urls as goal_urls
from social_django import urls as social_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include(core_urls)),
    path('goals/', include(goal_urls)),
    path('oauth/', include(social_urls, namespace='social')),
    path('bot/verify', BotVerifyView.as_view(), name='bot_verify'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema')),
]

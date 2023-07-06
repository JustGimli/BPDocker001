from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls',
         'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include('api.v1.urls')),
]


if settings.DEBUG:
    urlpatterns = [path('__debug__/', include(
        'debug_toolbar.urls'))] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

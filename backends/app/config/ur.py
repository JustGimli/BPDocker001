from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    # path('jet/dashboard/', include('jet.dashboard.urls',
    #      'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include('api.v1.urls')),
]

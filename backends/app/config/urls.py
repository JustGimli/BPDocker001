import os
from django.urls import path, include

if os.environ.get("PROD"):
    url = 'api/'
else:
    url = ''


urlpatterns = [
    path(f'{url}', include('config.u'))
]

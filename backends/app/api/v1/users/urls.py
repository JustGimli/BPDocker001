from django.urls import path
from .views import UserViewSet

urlpatterns = [
    path('getme/', UserViewSet.as_view({'get': 'list'})),
    path('update/', UserViewSet.as_view({'patch': 'update'}))
]


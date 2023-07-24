from django.urls import path
from .views import UserViewSet, get_user_profile, update_user

urlpatterns = [
    path('getme/', UserViewSet.as_view({'get': 'list'})),
    path('update/', UserViewSet.as_view({'patch': 'update'})),
    path('bot/get/', get_user_profile),
    path('bot/update/', update_user)
]

from django.urls import path
from .views import BotUsersViewSet, is_exists


urlpatterns = [
    path('create/',
         BotUsersViewSet.as_view({"post": "create"}),),
    path('me/', is_exists),
    path('update/', BotUsersViewSet.as_view({"post": "edit"}),)
]

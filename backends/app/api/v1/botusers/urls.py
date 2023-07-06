from django.urls import path
from .views import BotUsersViewSet, is_exists


urlpatterns = [
    path('create/',
         BotUsersViewSet.as_view()),
    path('me/', is_exists),
]

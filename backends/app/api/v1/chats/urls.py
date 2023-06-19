from django.urls import path

from .views import WebHooks, BotInfoHandler, ChatsViewSet, MessageListAPI, BotUsersViewSet, ConsultationViewSet

urlpatterns = [
    path('', WebHooks.as_view()),
    path('bot/', BotInfoHandler.as_view()),
    path('list/', ChatsViewSet.as_view({'get': 'list'})),
    path("create/", ChatsViewSet.as_view({'post': 'create'})),
    path('messages/<int:chat_id>/', MessageListAPI.as_view()),
    path('users/create/',
         BotUsersViewSet.as_view()),
    path('consultation/create/',
         ConsultationViewSet.as_view())
]

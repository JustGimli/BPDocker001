from django.urls import path

from .views import  BotInfoHandler, ChatsViewSet, MessageListAPI, WebHooks

urlpatterns = [
    path('', WebHooks.as_view()),
    path('bot/', BotInfoHandler.as_view()),
    path('list/', ChatsViewSet.as_view({'get': 'list'})),
    path("create/", ChatsViewSet.as_view({'post': 'create'})),
    path('messages/<int:chat_id>/', MessageListAPI.as_view()),
    

]

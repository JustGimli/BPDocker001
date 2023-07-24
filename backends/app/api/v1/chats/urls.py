from django.urls import path
from .views import BotInfoHandler, ChatsViewSet, MessageViewSet, WebHooks

urlpatterns = [
    path('', WebHooks.as_view()),
    path('bot/', BotInfoHandler.as_view()),
    path('list/', ChatsViewSet.as_view({'get': 'list'})),
    path('update/', ChatsViewSet.as_view({'patch': 'update'})),
    path("create/", ChatsViewSet.as_view({'post': 'create'})),
    path('messages/<int:chat_id>/', MessageViewSet.as_view({'get': 'list'})),
    path("messages/create/", MessageViewSet.as_view({'post': 'create'}))
]

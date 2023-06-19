import os
from django.urls import path, include
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from api.v1.chats.consumers import ChatConsumer


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter([
            path("api/ws/", ChatConsumer.as_asgi()),
        ])
    }
)

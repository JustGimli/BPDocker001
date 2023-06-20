from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()
from  api.v1.chats.sockets import websocket_urlpatterns




application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": URLRouter([
            websocket_urlpatterns
        ])
    }
)

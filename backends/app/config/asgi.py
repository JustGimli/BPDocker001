from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from  api.v1.chats.sockets import websocket_urlpatterns




application = ProtocolTypeRouter(
    {
        "https": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(URLRouter(websocket_urlpatterns))
    }
)

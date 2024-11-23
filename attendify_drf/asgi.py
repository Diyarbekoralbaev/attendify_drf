# attendify_drf/asgi.py

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import attendify_drf.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendify_drf.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            attendify_drf.routing.websocket_urlpatterns
        )
    ),
})

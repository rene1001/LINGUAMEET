"""
ASGI config for linguameet_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

# Ensure the Django settings module is set before importing any Django modules
# (especially routing/consumers which may import models and require settings).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "linguameet_project.settings")

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Initialize Django ASGI application first so apps are loaded before importing
# modules that may import models at import time (like consumers/routing).
django_asgi_app = get_asgi_application()

# Import websocket url patterns after Django apps are ready
from .routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

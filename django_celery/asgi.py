"""
ASGI config for django_celery project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from polls import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_celery.settings')


application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application(),
    # Websocket chat handler
    "websocket": URLRouter(
            routing.urlpatterns
        )
})


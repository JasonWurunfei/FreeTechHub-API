"""
ASGI config for FreeTechHub_api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from websocket.middleware import websockets

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FreeTechHub_api.settings')

application = get_asgi_application()
application = websockets(application)

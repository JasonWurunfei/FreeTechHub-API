# copied from https://medium.com/@alex.oleshkevich/websockets-in-django-3-1-73de70c5c1ba

from django.urls import resolve
from .connection import WebSocket

class LiveSockets:

    def __init__(self, socket_list):
        self._socket_list = socket_list

    def register(self, user_pk, socket):
        self._socket_list.append({
            "user_pk": user_pk,
            "socket": socket
        })

    def checkout(self, socket):
        for liveSocket in self._socket_list:
            if liveSocket['socket'] == socket:
                self._socket_list.remove(liveSocket)
    
    def get_socket(self, user_pk):
        for liveSocket in self._socket_list:
            if liveSocket['user_pk'] == user_pk:
                return liveSocket['socket']

        return None

    def __str__(self):
        return str(self._socket_list)

live_sockects = LiveSockets([])

def websockets(app):
    async def asgi(scope, receive, send):
        if scope["type"] == "websocket":
            match = resolve(scope["raw_path"].decode())
            await match.func(WebSocket(scope, receive, send),
                             live_sockects, *match.args, **match.kwargs)
            return
        await app(scope, receive, send)
    return asgi

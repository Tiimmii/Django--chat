from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'/socket-server/', ChatConsumer.as_asgi())
]
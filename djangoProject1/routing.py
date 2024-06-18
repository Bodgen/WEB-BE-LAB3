from django.urls import re_path

from .consumers import OnlineStatusConsumer, PostConsumer

websocket_urlpatterns = [
    re_path(r'ws/online/$', OnlineStatusConsumer.as_asgi()),
    re_path(r'ws/post/$', PostConsumer.as_asgi()),
]
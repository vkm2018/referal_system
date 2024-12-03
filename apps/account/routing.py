from django.urls import path

from . import consumers

# routing.py
from django.urls import re_path
from .consumers import InviteCodeConsumer

websocket_urlpatterns = [
    re_path(r'ws/notification/$', InviteCodeConsumer.as_asgi()),
]

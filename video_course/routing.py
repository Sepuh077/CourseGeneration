from django.urls import re_path

from .consumers import GeneratedTextConsumer

websocket_urlpatterns = [
    re_path(r"ws/process/(?P<room_name>[\w\-]+)/$", GeneratedTextConsumer.as_asgi()),
]

from django.conf.urls import re_path
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    re_path("ws/tuisong/(?P<category>[^/]+)", consumers.TuisongConsumer.as_asgi()),
    # path("ws/tuisong/", consumers.TuisongConsumer.as_asgi()),
]
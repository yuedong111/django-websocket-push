from django.conf.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path("ws/tuisong/(?P<category>[^/]+)", consumers.TuisongConsumer),
]
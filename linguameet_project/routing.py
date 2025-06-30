from django.urls import re_path
from conference.consumers import ConferenceConsumer

websocket_urlpatterns = [
    re_path(r'ws/conference/(?P<room_id>[^/]+)/$', ConferenceConsumer.as_asgi()),
] 
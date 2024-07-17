from django.urls import re_path, path
from Websocket import consumers

websocket_urlpatterns = [
    re_path(r'ws/updatejwt/(?P<room_name>\w+)/$',
            consumers.UpdateJWT.as_asgi()),
]

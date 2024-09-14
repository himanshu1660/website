from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('messages/', consumers.ChatConsumers.as_asgi()),
]
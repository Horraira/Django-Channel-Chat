from django.urls import path
from .consumers import ChatConsumer, NotificationConsumer

websocket_urlpatterns = [
    path('ws/notification/<str:room_name>/', ChatConsumer.as_asgi()),
    path("ws/notify/", NotificationConsumer.as_asgi()),
]
from django.urls import path

from . import consumer

websocket_urlpatterns = [
    path('ws/booking/<str:room_name>/', consumer.BookingConsumer),
]
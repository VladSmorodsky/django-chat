from django.urls.conf import path

from chat_app.ws.consumers import ChatConsumer

socker_urlpatterns = [
    path('ws/chat/<str:chat_id>/', ChatConsumer.as_asgi())
]

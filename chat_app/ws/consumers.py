from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async

from chat_app.constants import CHAT_NAME_PREFIX
from chat_app.models import Message, User, Chat


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        """
        Connect channel to chat
        :return:
        """
        print("Connected")
        user = self.scope['user']
        if not user.is_authenticated:
            await self.close()
            return
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'{CHAT_NAME_PREFIX}{self.chat_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive_json(self, text_data=None, bytes_data=None):
        """
        Retrieve and send message into group
        :param text_data:
        :param bytes_data:
        :return:
        """
        user = self.scope['user']
        messageText = text_data['message']
        message = await self.save_message(user, self.chat_id, messageText)
        channel_layer = get_channel_layer()
        await channel_layer.group_send(self.room_group_name,
                                       {'type': 'chat_message', 'message': messageText, 'username': user.email,
                                        'created_at': message.created_at.strftime('%H:%M %m %d, %Y')})

    async def chat_message(self, event):
        await self.send_json({
            'message': event['message'],
            'username': event['username'],
            'created_at': event['created_at'],
        })

    @database_sync_to_async
    def save_message(self, user: User, chat_id: int, message: str) -> Message:
        chat = Chat.objects.filter(id=chat_id).first()
        return Message.objects.create(user=user, chat=chat, message=message)

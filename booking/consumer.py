from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.authtoken.models import Token

import json

class BookingConsumer(AsyncWebsocketConsumer):
    username = ""
    token = ""
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'booking_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        try:
            self.token = text_data_json['token']
            self.username = await database_sync_to_async(self.get_username)()
            await self.channel_layer.group_send(
                self.room_group_name,
                {

                    'type': 'chat_message',
                    'message': message + "---" + self.username,
                    'username':self.username
                }
            )
        except Exception as e:
            print(e)
            await self.send(text_data=json.dumps({
                'message': "Authentication Error"
            }))
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        try:
            username = event['username']
            await self.send(text_data=json.dumps({
                    'message': message,
                    'username':username
            }))
        except Exception as e:
            print(e)
            await self.send(text_data=json.dumps({
                'message': "Authentication Error"
            }))

    def get_username(self):
        user = Token.objects.get(key=self.token).user
        return user.username

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from ChatApp.models import Room, Message


import base64
from django.core.files.base import ContentFile
from channels.db import database_sync_to_async
from django.core.files import File
from io import BytesIO

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        text_data = json.loads(text_data)
        file_data = text_data.get('file', None)

        # Convert file data back to ContentFile
        if file_data:
            file_name = file_data['name']
            file_content = BytesIO(bytearray(file_data['data']))
            file = ContentFile(file_content.read(), file_name)
        else:
            file = None
        
        # Save the message to the database (only by the sender)
        message_data = await self.create_message({
            'message': text_data['message'],
            'file': file,
            'sender': text_data['sender'],
            'room_name': text_data['room_name']
        })

        # Broadcast the message to the group
        event = {
            'type': 'send_message',
            'message': {
                'message': text_data['message'],
                'file_url': message_data['file_url'],  
                'sender': text_data['sender'],
                'room_name': text_data['room_name']
            },
        }
        await self.channel_layer.group_send(self.room_name, event)

    async def send_message(self, event):
        data = event['message']

        response_data = {
            'sender': data['sender'],
            'message': data['message'],
            'file_url': data['file_url']  # File URL from the sender's save operation
        }

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({'message': response_data}))

    @database_sync_to_async
    def create_message(self, data):
        room = Room.objects.get(room_name=data['room_name'])
        file = data['file']
        message_instance = Message.objects.create(
            room=room,
            sender=data['sender'],
            message=data['message'],
            file=file
        )
        return {
            'file_url': message_instance.file.url if file else None
        }


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'public_room'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({ 'message': event['message'] }))
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import Chat
from django.utils import timezone
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):


    @staticmethod
    @sync_to_async
    def cache_room(data):
        room_name = data.get('room_name')
        text = data.get('text')
        time = timezone.now()
        today = f'{time.month}/{time.day}'
        chat = get_object_or_404(Chat, room_name=room_name)
        message_id = 1 if not chat.messages else int([*chat.messages.values()][-1][-1]['message_id'])
        chat.messages.setdefault(today, [])
        init_data ={
            "sender": data.get('sender'),
            "text": text,
            "message_id": f'{message_id + 1}'
        }
        chat.messages[today].append(init_data)
        chat.save()
        print(chat)
        init_data['date'] = today
        return init_data


    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        data = await self.cache_room(text_data_json)
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", 'data': data}
        )

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['data']))
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, ChatMessage
from asgiref.sync import sync_to_async

from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user1_id = self.scope['url_route']['kwargs']['user1_id']
        user2_id = self.scope['url_route']['kwargs']['user2_id']
        chat_id = self.scope['url_route']['kwargs']['chat_id']

        # if self.scope['user'].id not in [user1_id, user2_id]:
        #     await self.close()
        #     return

        self.room_name = f"chat_{min(user1_id, user2_id)}_{max(user1_id, user2_id)}_{chat_id}"
        self.room_group_name = f"group_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )


    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        chatId = data['chatId']
        user1Id = data['user1Id']
        user2Id = data['user2Id']

        await self.save_message(username, message, chatId, user1Id, user2Id)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
            'type': 'chat_message',
            'message': message,
            'username': username,
            'chatId': chatId,
            'user1Id': user1Id,
            'user2Id': user2Id
            }
        )
    

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        chatId = event['chatId']
        user1Id = event['user1Id']
        user2Id = event['user2Id']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'chatId': chatId,
            'user1Id': user1Id,
            'user2Id': user2Id
        }))


    @sync_to_async
    def save_message(self, username, message, chatId, user1Id, user2Id):
        user = User.objects.get(username=username)
        chat = Chat.objects.get(id=chatId)
        sender = user if user.id in [user1Id, user2Id] else None

        if sender is not None and (sender.id == user1Id or sender.id == user2Id):
            ChatMessage.objects.create(chat=chat, sender=sender, content=message)


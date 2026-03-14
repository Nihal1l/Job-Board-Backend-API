import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
from users.serializers import UserSerializer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        
        # Check if user is authenticated via custom JWT middleware
        if not self.scope.get('user') or self.scope['user'].is_anonymous:
            await self.close()
            return
            
        self.user = self.scope['user']

        # Verify if the user is a part of this room
        is_participant = await self.is_room_participant(self.room_id, self.user)
        if not is_participant:
            await self.close()
            return

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

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json['message']

        # Save message to database
        message = await self.save_message(content)
        
        if not message:
            return

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'id': message.id,
                'message': content,
                'sender': await self.get_user_data(self.user),
                'timestamp': str(message.timestamp),
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']
        msg_id = event['id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'id': msg_id,
            'message': message,
            'sender': sender,
            'timestamp': timestamp
        }))

    @database_sync_to_async
    def is_room_participant(self, room_id, user):
        try:
            room = ChatRoom.objects.get(id=room_id)
            return user == room.employer or user == room.job_seeker
        except ChatRoom.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, content):
        try:
            room = ChatRoom.objects.get(id=self.room_id)
            message = Message.objects.create(room=room, sender=self.user, content=content)
            return message
        except Exception:
            return None

    @database_sync_to_async
    def get_user_data(self, user):
        from users.serializers import UserSerializer
        return UserSerializer(user).data

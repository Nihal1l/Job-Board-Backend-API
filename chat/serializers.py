from rest_framework import serializers
from .models import ChatRoom, Message
from users.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'content', 'timestamp', 'is_read']
        read_only_fields = ['id', 'timestamp', 'sender', 'room']

class ChatRoomSerializer(serializers.ModelSerializer):
    employer = UserSerializer(read_only=True)
    job_seeker = UserSerializer(read_only=True)
    latest_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'application', 'employer', 'job_seeker', 'created_at', 'latest_message']
        read_only_fields = ['id', 'created_at', 'employer', 'job_seeker']

    def get_latest_message(self, obj):
        message = obj.messages.order_by('-timestamp').first()
        if message:
            return MessageSerializer(message).data
        return None

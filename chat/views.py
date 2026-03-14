from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from job_seeker.models import appliedJobs

class ChatRoomListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(Q(employer=user) | Q(job_seeker=user)).order_by('-created_at')

    def perform_create(self, serializer):
        application_id = self.request.data.get('application')
        try:
            application = appliedJobs.objects.get(id=application_id)
            
            # Authorization Check
            user = self.request.user
            employer = application.job.user
            job_seeker = application.user
            
            if user != employer and user != job_seeker:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("You do not have permission to create this chat room.")
                
            # Check if chat room already exists
            chat_room = ChatRoom.objects.filter(application=application, employer=employer, job_seeker=job_seeker).first()
            if chat_room:
                 serializer.instance = chat_room
                 return # return existing, handled dynamically in view
            
            serializer.save(application=application, employer=employer, job_seeker=job_seeker)
        except appliedJobs.DoesNotExist:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"application": "Invalid application ID."})
            
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if hasattr(serializer, 'instance') and serializer.instance:
             return Response(ChatRoomSerializer(serializer.instance).data, status=status.HTTP_200_OK)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        user = self.request.user
        # Ensure user is part of the chat room
        try:
            room = ChatRoom.objects.get(id=room_id)
            if user != room.employer and user != room.job_seeker:
                return Message.objects.none()
            return Message.objects.filter(room=room).order_by('timestamp')
        except ChatRoom.DoesNotExist:
            return Message.objects.none()

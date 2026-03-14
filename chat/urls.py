from django.urls import path
from .views import ChatRoomListCreateView, MessageListView

urlpatterns = [
    path('rooms/', ChatRoomListCreateView.as_view(), name='chat-room-list-create'),
    path('rooms/<str:room_id>/messages/', MessageListView.as_view(), name='chat-room-messages'),
]

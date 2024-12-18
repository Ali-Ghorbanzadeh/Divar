from django.urls import path
from .views import CreateRetrieveChatAPIView, ChatListAPIView

urlpatterns = [
    path("chat/create/", CreateRetrieveChatAPIView.as_view(), name="get-or-create-room"),
    path("chat/<str:room_name>/", CreateRetrieveChatAPIView.as_view(), name="room"),
    path("chat/", CreateRetrieveChatAPIView.as_view(), name="chat-room"),
    path("chats/list/", ChatListAPIView.as_view(), name="chat-list")
]

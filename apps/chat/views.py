import string
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, get_object_or_404, GenericAPIView
from rest_framework.views import APIView
from .models import Chat
from .serializer import ChatSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from apps.advertisement.models import Ad
from apps.accounts.models import UserProfile
from random import randint, choices

class CreateRetrieveChatAPIView(RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_field = 'room_name'
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'chat/chat_room.html'

    def retrieve(self, request, *args, **kwargs):
        if not kwargs:
            return Response()
        response = super().retrieve(request, *args, **kwargs)
        if request.headers.get('Referer'):
            return JsonResponse(response.data)
        return response

    @staticmethod
    def generate_room_name():
        characters = string.ascii_letters + string.digits
        room_name = ''.join(choices(characters, k=randint(20, 40)))
        return room_name

    def post(self, request, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=request.data.get('ad'))
        if ad.connection_type == 'call_only':
            return Response({'message': 'You are not allowed to chat'}, status=status.HTTP_403_FORBIDDEN)
        owner = get_object_or_404(UserProfile, pk=request.data.get('owner'))
        if request.user == owner:
            return redirect('show-advertisement', pk=ad.id)

        instance, create = Chat.objects.get_or_create(advertise=ad, owner=owner, customer=request.user)
        if create:
            room_name = self.generate_room_name()
            instance.room_name = room_name
            instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

class ChatListAPIView(GenericAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get(self, request, *args, **kwargs):
        user = request.user.id
        owner_chats = Chat.objects.filter(owner=4)
        customer_chats = Chat.objects.filter(customer=4)
        all_chats = owner_chats.union(customer_chats)
        serializer = self.get_serializer(instance=all_chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
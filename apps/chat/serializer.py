from pkg_resources import require
from rest_framework.serializers import ModelSerializer
from .models import Chat

class ChatSerializer(ModelSerializer):

    class Meta:
        model = Chat
        fields = ['id',
                  'advertise',
                  'room_name',
                  'messages']
        extra_kwargs = {
            'messages': {'required': False, 'read_only': True},
        }
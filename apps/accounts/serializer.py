from rest_framework.serializers import ModelSerializer
from .models import UserProfile
from apps.advertisement.serializer import ListAdSerializer

class UserProfileSerializer(ModelSerializer):
    ads = ListAdSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
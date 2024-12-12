from rest_framework.serializers import ModelSerializer
from .models import UserProfile
from apps.advertisement.serializer import ListAdSerializer
from apps.advertisement.models import ProvinceOrCity


class UserProfileSerializer(ModelSerializer):
    ads = ListAdSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ["ads",
                  "first_name",
                  "last_name",
                  "email",
                  "phone_number",
                  "national_code",
                  "birthday",
                  "connection_type",
                  "premium",
                  "location",]

        extra_kwargs = {
            'username': {'required': False, 'read_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False, 'read_only': True},
            'phone_number': {'required': False},
            'national_code': {'required': False},
            'birthday': {'required': False},
            'connection_type': {'required': False},
            'premium': {'required': False, 'read_only': True},
            'location': {'required': False},
        }
        
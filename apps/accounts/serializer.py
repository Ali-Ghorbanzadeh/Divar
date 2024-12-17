from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import ModelSerializer
from .models import UserProfile, VerifyUser
from apps.advertisement.models import Image
from apps.advertisement.serializer import ListAdSerializer
from apps.advertisement.models import ProvinceOrCity, Ad


class UserProfileSerializer(ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ["first_name",
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

class UserAdHistorySerializer(ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['ads_history']


class UserVerificationSerializer(ModelSerializer):

    class Meta:
        model = VerifyUser
        fields = ['user_id']

    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist('images', [])
        assert images_data, 'حداقل باید یک عکس ارسال کنید'
        assert len(images_data) < 3, 'تعداد عکس ها بیش از حد مجاز است. حداکثر 2 عکس مجاز است.'
        instance = VerifyUser.objects.get_or_create(user_id=self.context['request'].data.get('user_id'))[0]
        object_id = instance.id
        content = ContentType.objects.get(model='verifyuser')
        images = [Image(content_type=content, object_id=object_id, src=image_data) for image_data in images_data]
        Image.objects.bulk_create(images)
        return instance
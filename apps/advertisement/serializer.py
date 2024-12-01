from rest_framework.serializers import ModelSerializer, SlugRelatedField
from .models import Category, Ad, Image, CategoryFields, Video
from django.contrib.contenttypes.models import ContentType


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ['src']


class CategoryFieldsSerializer(ModelSerializer):
    class Meta:
        model = CategoryFields
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    fields = CategoryFieldsSerializer(many=True)
    parent = SlugRelatedField(
        slug_field='title',
        read_only=True
    )

    class Meta:
        model = Category
        fields = '__all__'



class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = ['src']

class ListAdSerializer(ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Ad
        fields = ['id',
                  'title',
                  'images',
                  'premium',
                  'time_to_add']

class CreateUpdateRetrieveDeleteAdSerializer(ModelSerializer):
    videos = VideoSerializer(many=True, required=False)
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Ad
        fields = ['id',
                  'user',
                  'title',
                  'category',
                  'description',
                  'address',
                  'expire',
                  'connection_type',
                  'premium',
                  'images',
                  'videos',
                  'status',
                  'details',
                  'phone_number',
                  'total_count_view',
                  'time_to_add']

        extra_kwarg = {
            'description': {'required': False},
            'details': {'required': False},
            'connection_type': {'required': False},
            'expire': {'required': False, 'read_only': True},
            'premium': {'required': False, 'read_only': True},
            'images': {'required': False, 'read_only': True},
            'videos': {'required': False, 'read_only': True},
            'status': {'required': False, 'read_only': True},
            'total_count_view': {'required': False, 'read_only': True},
        }

    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist('images', [])
        videos_data = self.context['request'].FILES.getlist('videos', [])
        assert len(videos_data) < 3, 'تعداد ویدئوها بیش از حد مجاز است. حداکثر 2 ویدئو مجاز است.'
        assert len(images_data) + len(videos_data) < 6, 'حداکثر تعداد فایل ارسالی مجاز 5 عدد است.'
        instance = super().create(validated_data)
        object_id = instance.id
        content = ContentType.objects.get(model='ad')
        images = [Image(content_type=content, object_id=object_id, src=image_data) for image_data in images_data]
        videos = [Video(advertise=instance, src=video_data) for video_data in videos_data]
        Image.objects.bulk_create(images)
        Video.objects.bulk_create(videos)
        return instance

    def update(self, instance, validated_data):
        images_data = self.context['request'].FILES.getlist('images', [])
        videos_data = self.context['request'].FILES.getlist('videos', [])
        assert len(videos_data) < 3, 'تعداد ویدئوها بیش از حد مجاز است. حداکثر 2 ویدئو مجاز است.'
        assert len(images_data) + len(videos_data) < 6, 'حداکثر تعداد فایل ارسالی مجاز 5 عدد است.'
        validated_data['status'] = 'pending'
        super().update(instance, validated_data)
        object_id = instance.id
        content = ContentType.objects.get(model='ad')
        instance.videos.all().delete()
        instance.images.all().delete()
        images = [Image(content_type=content, object_id=object_id, src=image_data) for image_data in images_data]
        videos = [Video(advertise=instance, src=video_data) for video_data in videos_data]
        Image.objects.bulk_create(images)
        Video.objects.bulk_create(videos)
        return instance

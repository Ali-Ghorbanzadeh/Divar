from django.db import models
from datetime import timedelta
from django.utils import timezone
from config.settings import AUTH_USER_MODEL
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from apps.core.models import TimeStampMixin, LogicalDeleteMixin


class Category(TimeStampMixin, LogicalDeleteMixin):
    title = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='childes')
    premium = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class CategoryFields(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='fields')
    field_name = models.CharField(max_length=100)
    require = models.BooleanField(default=True)

    def __str__(self):
        return self.field_name


class ProvinceOrCity(TimeStampMixin, LogicalDeleteMixin):
    name = models.CharField(max_length=255)
    province = models.ForeignKey('self', on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name


class Ad(TimeStampMixin, LogicalDeleteMixin):

    TYPE_CHOICES = [
        ('chat_only', 'Chat'),
        ('call_only', 'Call'),
        ('both', 'Both'),
    ]

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=255, unique=True)
    category = models.OneToOneField(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=3000)
    address = models.ForeignKey(ProvinceOrCity, on_delete=models.CASCADE, related_name='ads')
    expire = models.DateTimeField(default=(timezone.now() + timedelta(days=30)))
    connection_type = models.CharField(choices=TYPE_CHOICES)
    premium = models.BooleanField(default=False)

    @property
    def detail(self):
        return self.details.values_list('attribute_name', 'attribute_value')

    def __str__(self):
        return self.title


class Image(TimeStampMixin, LogicalDeleteMixin):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='images')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    src = models.ImageField(upload_to=f'{content_type}/images/', null=True, blank=True)
    alt = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.src.url


class Video(TimeStampMixin, LogicalDeleteMixin):
    advertise = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='videos')
    src = models.FileField(upload_to=f'{advertise}/videos/', null=True, blank=True)
    alt = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.src.url


class AdDetail(models.Model):
    advertise = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='details')
    attribute_name = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.attribute_name}: {self.attribute_value}'

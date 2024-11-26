from django.db import models
from datetime import timedelta
from django.utils import timezone
from config.settings import AUTH_USER_MODEL
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from apps.core.models import TimeStampMixin, LogicalDeleteMixin
from time import time


class Category(TimeStampMixin, LogicalDeleteMixin):
    title = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='childes', null=True, blank=True)
    premium = models.BooleanField(default=False)

    @property
    def images(self):
        return Image.objects.filter(object_id=self.id, content_type__model='category').values('src')

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
    province = models.ForeignKey('self', on_delete=models.CASCADE, related_name='cities', null=True, blank=True)

    def __str__(self):
        return self.name


class Ad(TimeStampMixin, LogicalDeleteMixin):
    TYPE_CHOICES = [
        ('chat_only', 'Chat'),
        ('call_only', 'Call'),
        ('both', 'Both'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='advertisement')
    description = models.TextField(max_length=3000, null=True, blank=True)
    address = models.ForeignKey(ProvinceOrCity, on_delete=models.CASCADE, related_name='ads')
    expire = models.DateTimeField(default=(timezone.now() + timedelta(days=30)))
    connection_type = models.CharField(choices=TYPE_CHOICES, null=True, blank=True)
    premium = models.BooleanField(default=False)
    details = models.JSONField(null=True, blank=True)
    views = models.JSONField(null=True, blank=True)
    max_count_view = models.PositiveIntegerField(default=0)
    status = models.CharField(choices=STATUS_CHOICES, default='pending')

    @property
    def images(self):
        return Image.objects.filter(object_id=self.id, content_type__model='ad').values('src')

    @property
    def time_to_add(self):
        return int((timezone.now() - self.created_at).total_seconds())

    @property
    def count_views(self):
        if self.views:
            self.max_count_view = sum(self.views.values()) # NOQA
            self.save()
        return self.max_count_view

    @property
    def is_expire(self):
        return (timezone.now() - self.expire).total_seconds() > 0

    @property
    def phone_number(self):
        if self.connection_type == 'chat_only':
            return 'دسترسی به شماره تلفن کاربر مجاز نیست.'
        return self.user.phone_number

    @classmethod
    def get_ads(cls, category_title=None):
        if category_title:
            premium_ads = cls.objects.filter(premium=True, category__title=category_title)
            free_ads = cls.objects.filter(category__title=category_title).order_by('-created_at')
        else:
            premium_ads = cls.objects.filter(premium=True)
            free_ads = cls.objects.filter().order_by('-created_at')
        if not all((premium_ads, free_ads)):
            return cls.get_ads()
        max_view = max([ad.count_views for ad in premium_ads])
        premiums = premium_ads.filter(max_count_view__lt=max_view + 1).order_by('max_count_view')[:3]
        all_ads = [*premiums, *free_ads.exclude(id__in=premiums.values('id'))]
        return all_ads

    def __str__(self):
        return self.title


class Image(TimeStampMixin, LogicalDeleteMixin):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='images')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    src = models.ImageField(upload_to='images/')

    def delete(self, using=None, keep_parents=False):
        # delete file # TODO
        return super().delete(using, keep_parents)

    def __str__(self):
        return self.src.url


class Video(TimeStampMixin, LogicalDeleteMixin):
    advertise = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='videos')
    src = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.src.url

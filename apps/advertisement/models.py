from django.db import models
from datetime import timedelta
from django.utils import timezone
from config.settings import AUTH_USER_MODEL
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from apps.core.models import TimeStampMixin, LogicalDeleteMixin
from django.contrib.postgres.fields import ArrayField
from django.core.cache import caches
from django.utils.connection import ConnectionProxy
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

cache = ConnectionProxy(caches, 'advertisements')

class Category(TimeStampMixin, LogicalDeleteMixin):
    title = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='childes', null=True, blank=True)
    premium = models.BooleanField(default=False)
    images = GenericRelation('Image')

    def __str__(self):
        return self.title


class CategoryFields(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='fields')
    field_name = models.CharField(max_length=100)
    require = models.BooleanField(default=True)

    def clean(self, *args, **kwargs):
        if self.category.childes:
            raise ValidationError(
                _("Invalid value: %(value)s, The field group can only belong to the last subgroup"),
                params={"value": args},
            )



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
    details = models.JSONField(default=dict, null=True, blank=True)
    views = models.JSONField(default=dict, null=True, blank=True)
    total_count_view = models.PositiveIntegerField(default=0)
    status = models.CharField(choices=STATUS_CHOICES, default='pending')
    viewed_users = ArrayField(models.CharField(max_length=255), default=list)
    images = GenericRelation('Image')

    @property
    def time_to_add(self):
        return int((timezone.now() - self.created_at).total_seconds())


    @property
    def phone_number(self):
        if self.connection_type == 'chat_only':
            return 'دسترسی به شماره تلفن کاربر مجاز نیست.'
        return self.user.phone_number

    @classmethod
    def get_ads(cls, order_by='-created_at', **kwargs):
        key = list(kwargs.values())
        key.append(order_by)
        key = '>'.join(key)

        if data := cache.get(key):
            return data

        premium_ads = cls.objects.filter(premium=True, **kwargs)
        free_ads = cls.objects.filter(**kwargs).order_by(order_by)

        if not free_ads:
            return cls.get_ads()

        max_view = 0

        if premium_ads:
            max_view = max([ad.total_count_view for ad in premium_ads])

        premiums = premium_ads.filter(total_count_view__lte=max_view).order_by('total_count_view')[:3]

        all_ads = [*premiums, *free_ads.exclude(id__in=premiums.values('id'))]
        cache.set(key=key, value=all_ads, timeout=30)
        return all_ads

    def clean(self, *args, **kwargs):
        if not all([self.user.first_name, self.user.last_name, self.user.national_code, self.user.phone_number]):
            raise ValidationError(
                _("Before registering an ad, you must complete your profile information")
            )
        if self.address.cities:
            raise ValidationError(
                _("Before registering an ad, you must complete your profile information")
            )

    def __str__(self):
        return self.title


class Image(TimeStampMixin):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='images')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    src = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.src.url


class Video(TimeStampMixin):
    advertise = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='videos')
    src = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.src.url

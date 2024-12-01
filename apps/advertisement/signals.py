from django.dispatch import receiver
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from .models import Image, Video, Ad
from django.db.models.signals import pre_save, post_delete
from apps.core.utils.exceptions import CustomAPIException


@receiver(post_delete)
def delete_file(sender, instance, **kwargs):
    if sender == Image or sender == Video:
        instance.src.delete(False)


# @receiver(pre_save, sender=Ad)
# def check_ad_count(sender, instance, *args, **kwargs):
#     print(args)
#     print(kwargs)
#     print(sender)
#     print(instance)
#     if created:
#         if len(Ad.objects.archive().filter(user=instance.user, created_at__gt=timezone.now() - timedelta(days=30))) > 6:
#             del instance
#             raise CustomAPIException('شما مجاز به ثبت بیش از 6 آگهی نیستید در بازه زمانی 30 روزه نیستید!', status.HTTP_400_BAD_REQUEST)
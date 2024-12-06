from celery import shared_task
from .models import Ad
from django.utils import timezone

@shared_task
def check_expire_ad():
    print('Checking expire ad')
    objects = Ad.objects.filter(expire__lt=timezone.now()).delete()
    print(objects)

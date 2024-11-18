from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampMixin
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True)
    book_mark = models.ForeignKey('advertisement.Ad',on_delete=models.CASCADE,
                                  null=True, blank=True, related_name='favorite_ad')
    national_code = models.CharField(max_length=10, unique=True)
    birthday = models.DateField(null=True, blank=True)
    connection_type = models.CharField(default='chat_only')
    premium = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class VerifyUser(TimeStampMixin):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='verify')
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


# class Notifications(TimeStampMixin):
    # user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications')
    # message = models.TextField()
    # status = models.BooleanField(default=True)
    #
    # @property
    # def elapsed_time(self):
    #     day = timezone.now().day - self.created_at.day
    #     hour = timezone.now().hour - self.created_at.hour
    #     return day, hour
    #
    # def __str__(self):
    #     return self.message

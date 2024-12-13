from django.contrib.auth.hashers import make_password
from django.db import models
from apps.core.models import TimeStampMixin
from django.contrib.auth.models import AbstractUser, UserManager
from apps.advertisement.models import ProvinceOrCity
from django.utils.translation import gettext_lazy as _
from apps.advertisement.models import Ad

class CustomUserManager(UserManager):
    def _create_user(self, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        password = extra_fields.pop("password")
        user = self.model(**extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(**extra_fields)

    def create_superuser(self, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(**extra_fields)

class UserProfile(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True)
    book_mark = models.JSONField(null=True, blank=True)
    national_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    location = models.ForeignKey(ProvinceOrCity, null=True, blank=True, on_delete=models.SET_NULL)
    connection_type = models.CharField(default='chat_only')
    premium = models.BooleanField(default=False)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def ads_history(self):
        ads = Ad.objects.archive().filter(user=self).values('id', 'title', 'status', 'premium').order_by('-created_at')
        Ad.objects.all().values()
        return ads

    def __str__(self):
        return self.email


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

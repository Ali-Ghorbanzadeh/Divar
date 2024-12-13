from django.core.validators import MinValueValidator
from django.db import models
from apps.core.models import TimeStampMixin
from apps.advertisement.models import Ad


class Flags(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField(validators=[MinValueValidator(1_000)])


class Payment(TimeStampMixin):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed')
    ]

    advertise = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='payments')
    flag = models.ForeignKey(Flags, on_delete=models.CASCADE, related_name='payments')
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=20)


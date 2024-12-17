from django.db import models
from apps.core.models import TimeStampMixin
from django.conf import settings
from apps.advertisement.models import Ad
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Chat(TimeStampMixin):
    advertise = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='chats')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner_chats')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_chats')
    room_name = models.TextField(unique=True, null=True, blank=True)
    messages = models.JSONField(default=dict)

    # class Meta:
    #     unique_together = ('advertise', 'owner', 'customer')

    def clean(self):
        if self.advertise.connection_type == 'call_only':
            raise ValidationError(_('You cannot set up a chat room for ads that "connection_type" is "call_only" !'))

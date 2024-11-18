from django.db import models


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LogicalDeleteMixin(models.Model):
    is_deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        if not self.is_deleted:
            self.is_deleted = True
            self.save(update_fields=["is_deleted"])

    class Meta:
        abstract = True

from django.apps import AppConfig


class AdvertisementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.advertisement'

    def ready(self):
        import apps.advertisement.signals
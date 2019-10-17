from django.apps import AppConfig
from django.conf import settings

class BaseConfig(AppConfig):
    name = 'base'

    def ready(self):
        from . import checks
        from base.signals import image_publish
        if settings.ISSTAGING or settings.ISPRODUCTION:
            from base.signals import aws_publish
        elif settings.ISREVIEWAPP:
            from base.signals import netlify_publish

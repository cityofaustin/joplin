from django.apps import AppConfig
from django.conf import settings


class BaseConfig(AppConfig):
    name = 'base'

    def ready(self):
        from . import checks
        from base.signals import image_publish
        from base.signals import janis_post_signals
        if settings.ISSTAGING or settings.ISPRODUCTION:
            from base.signals import aws_publish
        # Can't publish from LOCAL environment. A deployed Janis couldn't ping your localhost:8000
        elif settings.ISREVIEW:
            from base.signals import netlify_publish

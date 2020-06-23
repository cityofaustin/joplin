from django.apps import AppConfig
from django.conf import settings


class BaseConfig(AppConfig):
    name = 'base'

    def ready(self):
        from . import checks
        from base.signals import image_publish
        from base.signals import janis_build_triggers

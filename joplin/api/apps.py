from django.apps import AppConfig


class APIConfig(AppConfig):
    name = 'api'

    def ready(self):
        from . import checks

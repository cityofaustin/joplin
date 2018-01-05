from django.core.checks import Error, register
from django.conf import settings

from . import schema


@register()
def check_supported_langs(app_configs, **kwargs):
    errors = []

    for lang in settings.SUPPORTED_LANGS:
        try:
            schema.Language.get(lang)
        except ValueError as e:
            errors.append(
                Error(str(e), hint=f'Define "{lang}" as an enum option in schema.Language or remove "{lang}" from settings.SUPPORTED_LANGS', obj=schema.Language)
            )

    return errors

import pprint

from django.core.checks import Error, register
from django.conf import settings, global_settings


@register()
def check_language_count(app_configs, **kwargs):
    errors = []

    if len(settings.SUPPORTED_LANGS) != len(settings.LANGUAGES):
        msg = f'Expected settings.SUPPORTED_LANGS (count={len(settings.SUPPORTED_LANGS)}) to be the same length as settings.LANGUAGES (count={len(settings.LANGUAGES)})'
        hint = f'Ensure the requested languages {pprint.pformat(settings.SUPPORTED_LANGS)} are in django.global_settings.LANGUAGES'
        errors.append(
            Error(msg, hint=hint, obj='settings')
        )

    return errors

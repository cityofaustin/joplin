from django.db import models
from django.conf import settings
from wagtail.contrib.settings.models import BaseSetting, register_setting

@register_setting
class JanisBranchSettings(BaseSetting):
    preview_janis_branch = models.TextField(
        help_text='Janis branch to preview pages',
        blank=True,
        null=True,
    )
    publish_janis_branch = models.TextField(
        help_text='Janis branch to publish pages',
        blank=True,
        null=True,
    )

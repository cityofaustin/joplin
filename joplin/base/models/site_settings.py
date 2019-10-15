from django.db import models
from django.conf import settings
from wagtail.contrib.settings.models import BaseSetting, register_setting

# Used to set preview_janis_branch and publish_janis_branch for Local and PR Review Apps
# Staging and Production will use hardcoded JANIS_URL environment variable
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

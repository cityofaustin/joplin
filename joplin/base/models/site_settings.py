from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class JanisBranchSettings(BaseSetting):
    janis_branch = models.URLField(
        help_text='branch to build janis on publish')

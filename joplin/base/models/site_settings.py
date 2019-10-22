import re
from django.db import models
from django.conf import settings
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting

# Used to set preview_janis_branch and publish_janis_branch for Local and PR Review Apps
# Staging and Production will use hardcoded JANIS_URL environment variable
@register_setting
class JanisBranchSettings(BaseSetting):
    preview_input = models.CharField(
        verbose_name="Preview Input Options",
        choices=(('url', 'Url'), ('branch_name', 'Branch Name')),
        max_length=11,
        default="url",
        blank=False,
    )
    preview_janis_url = models.URLField(
        verbose_name='Preview Janis URL',
        help_text='Url of deployed Janis branch to preview pages. Ex: "https://janis.austintexas.io", "localhost:3000" (Don\'t add quotes)',
        blank=True,
        null=True,
    )
    preview_janis_branch = models.TextField(
        verbose_name='Preview Janis Branch Name',
        help_text='Name of Janis branch to preview pages. Ex: "3000-my-issue-name" (Don\'t add quotes)',
        blank=True,
        null=True,
    )
    publish_janis_branch = models.TextField(
        verbose_name='Publish Janis Branch Name',
        help_text='Name of Janis branch you want to publish to. Ex: "3000-my-issue-name" (Don\'t add quotes)',
        blank=True,
        null=True,
    )
    panels = [
        FieldPanel('preview_input'),
        FieldPanel('preview_janis_url', classname='preview_janis_url-container'),
        FieldPanel('preview_janis_branch', classname='preview_janis_branch-container'),
        FieldPanel('publish_janis_branch'),
    ]

    # Convert branch name to a netlify URL
    def branch_preview_url_base(self):
        if self.preview_input == "url":
            return self.preview_janis_url
        else:
            # Netlify site names are limited to 63 characters
            return f"https://{('janis-' + self.preview_janis_branch)[:63]}.netlify.com"

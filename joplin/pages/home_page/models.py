import re
from django.db import models
from django.conf import settings
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel


class HomePage(Page):
    parent_page_types = []
    subpage_types = []

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

    content_panels = [
        FieldPanel('preview_janis_branch'),
        FieldPanel('publish_janis_branch'),
    ]


    # branch_type is either "publish_janis_branch" or "preview_janis_branch"
    def __get_url_for_pr(self, branch_type):
        branch = getattr(self, branch_type)
        if not branch:
            # TODO: find a better way to handle missing values
            return "http://fake.base.url"
        else:
            # Netlify site names are limited to 63 characters
            return f"https://{('janis-v3-' + getattr(self, branch_type).lower())[:63]}.netlify.app"


    def preview_url_base(self):
        if settings.ISSTAGING or settings.ISPRODUCTION:
            return settings.JANIS_URL
        else:
            return self.__get_url_for_pr("preview_janis_branch")


    def publish_url_base(self):
        if settings.ISSTAGING or settings.ISPRODUCTION:
            return settings.JANIS_URL
        else:
            return self.__get_url_for_pr("publish_janis_branch")

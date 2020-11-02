import re
from django.db import models
from django.conf import settings
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.core.models import Orderable
from modelcluster.fields import ParentalKey
from pages.information_page.models import InformationPage
from pages.service_page.models import ServicePage
from pages.guide_page.models import GuidePage
from pages.official_documents_collection.models import OfficialDocumentCollection


class HomePage(Page):
    parent_page_types = []

    preview_janis_branch_for_pr = models.TextField(
        verbose_name='Preview Janis Branch Name',
        help_text='Name of Janis branch to preview pages. Ex: "3000-my-issue-name" (Don\'t add quotes)',
        blank=True,
        null=True,
    )

    publish_janis_branch_for_pr = models.TextField(
        verbose_name='Publish Janis Branch Name',
        help_text='Name of Janis branch you want to publish to. Ex: "3000-my-issue-name" (Don\'t add quotes)',
        blank=True,
        null=True,
    )

    content_panels = [
        InlinePanel('top_pages', heading='Links to top services', label='top link',
                    help_text='Add links to 1-4 top service pages (4 maximum allowed).',
                    min_num=None, max_num=4),
        FieldPanel('preview_janis_branch_for_pr'),
        FieldPanel('publish_janis_branch_for_pr'),
    ]


    # branch_type is either "publish_janis_branch_for_pr" or "preview_janis_branch_for_pr"
    def __get_url_for_pr(self, branch_type):
        branch = getattr(self, branch_type)
        if not branch:
            # TODO: find a better way to handle missing values
            return "http://fake.base.url"
        else:
            # Netlify site names are limited to 63 characters
            return f"https://{('janis-v3-' + branch.lower())[:63]}.netlify.com"


    # On staging and production, preview_url_base is set by JANIS_URL environment variable.
    # On Local and PR apps, its set by preview_janis_branch_for_pr on HomePage model.
    # preview_url_base() is used for "Preview" links in Joplin UI.
    def preview_url_base(self):
        if settings.IS_STAGING or settings.IS_PRODUCTION:
            return settings.JANIS_URL
        else:
            return self.__get_url_for_pr("preview_janis_branch_for_pr")


    # On staging and production, publish_url_base is set by JANIS_URL environment variable.
    # On Local and PR apps, its set by publish_janis_branch_for_pr on HomePage model.
    # publish_url_base() is used for "View Live" links in Joplin UI.
    def publish_url_base(self):
        if settings.IS_STAGING or settings.IS_PRODUCTION:
            return settings.JANIS_URL
        else:
            return self.__get_url_for_pr("publish_janis_branch_for_pr")


    # On staging and production, publish_janis_branch is set by JANIS_URL environment variable.
    # On Local and PR apps, its set by publish_janis_branch_for_pr on HomePage model.
    # publish_janis_branch() is used for publishing by base/signals/janis_build_triggers.py
    def publish_janis_branch(self):
        if settings.IS_STAGING:
            return "master"
        elif settings.IS_PRODUCTION:
            return "production"
        else:
            return getattr(self, "publish_janis_branch_for_pr")


class HomePageTopPage(Orderable):
    home_page = ParentalKey(HomePage, related_name='top_pages')
    page = models.ForeignKey('wagtailcore.Page', verbose_name='Select a page', related_name='+', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('page', page_type=[ServicePage]),
    ]

    def __str__(self):
        return self.page.title

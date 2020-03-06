from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import PageChooserPanel

from base import forms as custom_forms

from .translated_image import TranslatedImage
from .contact import Contact, ContactDayAndDuration, PhoneNumber
from .day_and_duration import DayAndDuration
from .location import Location
from .map import Map
from .constants import WYSIWYG_GENERAL, DEFAULT_MAX_LENGTH, SHORT_DESCRIPTION_LENGTH

from pages.base_page.models import JanisBasePage
from .home_page import HomePage
from .theme import Theme
from pages.topic_collection_page.models import TopicCollectionPage
from .widgets import countMe, countMeTextArea
from .site_settings import JanisBranchSettings
from .deployment_log import DeploymentLog

# TODO: Remove everything below this comment


class TopicCollectionPageTopicCollection(ClusterableModel):
    page = ParentalKey(TopicCollectionPage, related_name='topiccollections')
    topiccollection = models.ForeignKey(
        TopicCollectionPage, verbose_name='Select a Topic Collection', related_name='+', on_delete=models.CASCADE)
    panels = [
        PageChooserPanel('topiccollection'),
    ]

    def __str__(self):
        return self.topiccollection.text


@register_snippet
class ThreeOneOne(ClusterableModel):
    title = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    url = models.URLField()

    def __str__(self):
        return self.title

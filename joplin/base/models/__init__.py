from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import PageChooserPanel

from .translated_image import TranslatedImage
from .map import Map
from .constants import WYSIWYG_GENERAL, DEFAULT_MAX_LENGTH, SHORT_DESCRIPTION_LENGTH

from .theme import Theme
from pages.topic_collection_page.models import TopicCollectionPage
from pages.home_page.models import HomePage
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

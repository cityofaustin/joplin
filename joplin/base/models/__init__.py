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
        'base.TopicCollectionPage', verbose_name='Select a Topic Collection', related_name='+', on_delete=models.CASCADE)

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


# I tried to remove the ProcessPages, but ended up getting errors with old migrations. - chia 1/22/20
class ProcessPage(JanisBasePage):
    janis_url_page_type = "processes"

    department = models.ForeignKey(
        'base.DepartmentPage',
        on_delete=models.PROTECT,
        verbose_name='Select a Department',
        blank=True,
        null=True,
    )

    description = models.TextField(blank=True)
    image = models.ForeignKey(TranslatedImage, null=True,
                              blank=True, on_delete=models.SET_NULL, related_name='+')
    # TODO: Add images array field

    content_panels = [
        InlinePanel('topics', label='Topics'),
        FieldPanel('department'),
        FieldPanel('description', widget=countMeTextArea),
        ImageChooserPanel('image'),
        InlinePanel('contacts', label='Contacts'),
        InlinePanel('process_steps', label="Process steps"),
    ]


class ProcessPageStep(Orderable):
    page = ParentalKey(ProcessPage, related_name='process_steps')
    title = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    short_title = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    link_title = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    description = models.TextField(blank=True)
    image = models.ForeignKey(TranslatedImage, null=True,
                              blank=True, on_delete=models.SET_NULL, related_name='+')
    overview_steps = RichTextField(
        features=WYSIWYG_GENERAL, verbose_name='Write out the steps a resident needs to take to use the service', blank=True)
    detailed_content = RichTextField(
        features=WYSIWYG_GENERAL, verbose_name='Write any detailed content describing the process', blank=True)
    quote = models.TextField(blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('short_title'),
        FieldPanel('link_title'),
        FieldPanel('description', widget=countMeTextArea),
        ImageChooserPanel('image'),
        FieldPanel('overview_steps'),
        FieldPanel('detailed_content'),
        FieldPanel('quote'),
    ]


class ProcessPageContact(ClusterableModel):
    process = ParentalKey(ProcessPage, related_name='contacts')
    contact = models.ForeignKey(
        Contact, related_name='+', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('contact'),
    ]

    def __str__(self):
        return self.contact.name


class ProcessPageTopic(ClusterableModel):
    page = ParentalKey(ProcessPage, related_name='topics')
    topic = models.ForeignKey(
        'base.TopicPage', verbose_name='Select a Topic', related_name='+', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('topic'),
    ]

    def __str__(self):
        return self.topic.text

from django.db import models
import os
import graphene

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.utils.decorators import cached_classmethod
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface, HelpPanel
from wagtail.core.blocks import TextBlock, RichTextBlock, ListBlock, StreamBlock, StructBlock, URLBlock, PageChooserBlock, CharBlock
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail.admin.edit_handlers import PageChooserPanel

from base import blocks as custom_blocks
from base import forms as custom_forms

from .translated_image import TranslatedImage
from .contact import Contact, ContactDayAndDuration, PhoneNumber
from .day_and_duration import DayAndDuration
from .location import Location
from .map import Map

from .janis_page import JanisBasePage
from .home_page import HomePage
from .theme import Theme
from .topic_collection_page import TopicCollectionPage
from .topic_page import TopicPage, TopicPageTopicCollection
from .service_page import ServicePage, ServicePageTopic, ServicePageContact, ServicePageRelatedDepartments
from .information_page import InformationPage, InformationPageRelatedDepartments, InformationPageTopic, InformationPageContact
from .department_page import DepartmentPage, DepartmentPageDirector, DepartmentPageContact
from .official_documents_page import OfficialDocumentPage, OfficialDocumentPageOfficialDocument, OfficialDocumentPageRelatedDepartments, OfficialDocumentPageTopic
from .guide_page import GuidePage, GuidePageTopic, GuidePageRelatedDepartments, GuidePageContact

WYSIWYG_GENERAL = ['h1', 'h2', 'h3', 'h4', 'bold', 'link', 'ul', 'ol', 'code']
DEFAULT_MAX_LENGTH = 255
SHORT_DESCRIPTION_LENGTH = 300


# TODO: Remove everything below this comment

class TopicCollectionPageTopicCollection(ClusterableModel):
    page = ParentalKey(TopicCollectionPage, related_name='topiccollections')
    topiccollection = models.ForeignKey(
        'base.TopicCollectionPage',  verbose_name='Select a Topic Collection', related_name='+', on_delete=models.CASCADE)

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

    base_form_class = custom_forms.ProcessPageForm

    content_panels = [
        InlinePanel('topics', label='Topics'),
        FieldPanel('department'),
        FieldPanel('description'),
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
        FieldPanel('description'),
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
        'base.TopicPage',  verbose_name='Select a Topic', related_name='+', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('topic'),
    ]

    def __str__(self):
        return self.topic.text


@register_snippet
class Department(ClusterableModel):
    slug = models.SlugField()
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    mission = models.TextField()
    image = models.ForeignKey(
        TranslatedImage, null=True, on_delete=models.SET_NULL, related_name='+')

    panels = [
        FieldPanel('name'),
        FieldPanel('mission'),
        InlinePanel('contacts', label='Contacts'),
        ImageChooserPanel('image'),
    ]

    def __str__(self):
        return self.name


class DepartmentContact(ClusterableModel):
    department = ParentalKey(Department, related_name='contacts')
    contact = models.ForeignKey(
        Contact, related_name='+', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('contact'),
    ]

    def __str__(self):
        return self.department.name

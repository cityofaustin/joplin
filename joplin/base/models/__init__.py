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
from .constants import WYSIWYG_GENERAL, DEFAULT_MAX_LENGTH, SHORT_DESCRIPTION_LENGTH

from .janis_page import JanisBasePage
from .home_page import HomePage
from .theme import Theme
from .topic_collection_page import TopicCollectionPage
from .topic_page import TopicPage, TopicPageTopicCollection, TopicPageTopPage
from .service_page import ServicePage, ServicePageTopic, ServicePageContact, ServicePageRelatedDepartments
from .information_page import InformationPage, InformationPageRelatedDepartments, InformationPageTopic, InformationPageContact
from .department_page import DepartmentPage, DepartmentPageDirector, DepartmentPageContact, DepartmentPageTopPage, DepartmentPageRelatedPage
from .official_documents_page import OfficialDocumentPage, OfficialDocumentPageOfficialDocument, OfficialDocumentPageRelatedDepartments, OfficialDocumentPageTopic
from .guide_page import GuidePage, GuidePageTopic, GuidePageRelatedDepartments, GuidePageContact
from .form_container import FormContainer, FormContainerRelatedDepartments, FormContainerTopic
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

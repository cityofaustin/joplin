from django.db import models

from modelcluster.models import ClusterableModel

from wagtail.api import APIField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsnippets.models import register_snippet

from . import blocks as custom_blocks
from . import forms as custom_forms


class HomePage(Page):
    parent_page_types = []
    subpage_types = ['base.ServicePage']


WYSIWYG_FEATURES = ['h1', 'h2', 'link', 'ul', 'ol']
DEFAULT_MAX_LENGTH = 255


class ServicePage(Page):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    content = RichTextField(features=WYSIWYG_FEATURES, verbose_name='Write out the steps a resident needs to take to use the service')
    extra_content = StreamField(
        [
            ('content', blocks.RichTextBlock(features=WYSIWYG_FEATURES, help_text='Write any additional content describing the service')),
            ('application_block', custom_blocks.SnippetChooserBlockWithAPIGoodness('base.ApplicationBlock')),
        ],
        verbose_name='Add any forms, maps, apps, or content that will help the resident use the service',
    )
    theme = models.ForeignKey(
        'base.Theme',
        on_delete=models.PROTECT,
        related_name='+'
    )

    parent_page_types = ['base.HomePage']
    subpage_types = []
    base_form_class = custom_forms.ServicePageForm

    content_panels = [
        FieldPanel('theme'),
        FieldPanel('title'),
        FieldPanel('content'),
        StreamFieldPanel('extra_content'),
    ]

    api_fields = [
        APIField('content'),
        APIField('extra_content'),
        APIField('theme'),
    ]

    es_panels = [
        # TODO: This field comes from Page and django-modeltranslation complains about it
        # FieldPanel('title_es'),
        FieldPanel('content_es'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(es_panels, heading='Spanish', classname='translation-tab'),
        ObjectList(Page.promote_panels, heading='Promote'),
        # TODO: What should we do with the fields in settings?
        # ObjectList(Page.settings_panels, heading='Settings', classname='settings'),
    ])


@register_snippet
class Theme(ClusterableModel):
    text = models.CharField(max_length=DEFAULT_MAX_LENGTH)

    api_fields = ['text']

    def __str__(self):
        return self.text


@register_snippet
class ApplicationBlock(ClusterableModel):
    url = models.URLField()
    description = models.TextField()

    panels = [
        FieldPanel('url'),
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.description


@register_snippet
class Event(ClusterableModel):
    title = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    address = models.TextField()
    fees = models.CharField(max_length=DEFAULT_MAX_LENGTH)


@register_snippet
class Director(ClusterableModel):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    photo = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    email = models.EmailField()
    phone_number = models.CharField(max_length=DEFAULT_MAX_LENGTH)


@register_snippet
class Department(ClusterableModel):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    address = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    hours = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    phone_number = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.name


@register_snippet
class Location(ClusterableModel):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    address = models.TextField()
    hours = models.CharField(max_length=DEFAULT_MAX_LENGTH)


@register_snippet
class Contact(ClusterableModel):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    email = models.EmailField()
    phone_number = models.CharField(max_length=DEFAULT_MAX_LENGTH)

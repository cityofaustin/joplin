from django.db import models

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.api import APIField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock
from wagtail.wagtailsnippets.models import register_snippet

from taggit.models import TaggedItemBase


class HomePage(Page):
    pass


WYSIWYG_FEATURES = ['h1', 'h2', 'h3', 'bold', 'italic', 'link', 'ul', 'ol']


class ServicePage(Page):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    content = RichTextField(features=WYSIWYG_FEATURES, help_text='Write out the steps a resident needs to take to use the service')
    extra_content = StreamField([
        ('content', blocks.RichTextBlock(features=WYSIWYG_FEATURES, help_text='Write any additional content describing the service')),
        ('application_block', SnippetChooserBlock('base.ApplicationBlock')),
    ])
    tags = ClusterTaggableManager(through='base.ServicePageTag', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('content', classname='full'),
        StreamFieldPanel('extra_content'),
        FieldPanel('tags'),
    ]

    api_fields = [
        APIField('content'),
        APIField('extra_content'),
        APIField('tags'),
    ]


class ServicePageTag(TaggedItemBase):
    content_object = ParentalKey('base.ServicePage', related_name='tagged_items')


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
    title = models.CharField(max_length=255)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    address = models.TextField()
    fees = models.CharField(max_length=255)


@register_snippet
class Director(ClusterableModel):
    name = models.CharField(max_length=255)
    photo = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)


@register_snippet
class Department(ClusterableModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    hours = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.name


@register_snippet
class Location(ClusterableModel):
    name = models.CharField(max_length=255)
    address = models.TextField()
    hours = models.CharField(max_length=255)


@register_snippet
class Contact(ClusterableModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)

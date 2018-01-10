from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.api import APIField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
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
    topic = models.ForeignKey(
        'base.Topic',
        on_delete=models.PROTECT,
        related_name='services',
    )

    parent_page_types = ['base.HomePage']
    subpage_types = []
    base_form_class = custom_forms.ServicePageForm

    content_panels = [
        FieldPanel('topic'),
        FieldPanel('title'),
        FieldPanel('content'),
        StreamFieldPanel('extra_content'),
        InlinePanel('contacts', label='Contacts'),
    ]

    api_fields = [
        APIField('content'),
        APIField('extra_content'),
        APIField('topic'),
        APIField('contacts'),
    ]

    es_panels = [
        # TODO: This field comes from Page and django-modeltranslation complains about it
        # FieldPanel('title_es'),
        FieldPanel('content_es'),
    ]

    vi_panels = [
        # TODO: This field comes from Page and django-modeltranslation complains about it
        # FieldPanel('title_es'),
        FieldPanel('content_vi'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(es_panels, heading='Spanish', classname='translation-tab'),
        ObjectList(vi_panels, heading='Vietnamese', classname='translation-tab'),
        ObjectList(Page.promote_panels, heading='Promote'),
        # TODO: What should we do with the fields in settings?
        # ObjectList(Page.settings_panels, heading='Settings', classname='settings'),
    ])


@register_snippet
class Topic(ClusterableModel):
    text = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    description = models.TextField()

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
class Location(ClusterableModel):
    TX = 'TX'
    STATE_CHOICES = (
        (TX, 'Texas'),
    )

    USA = 'United States'
    COUNTRY_CHOICES = (
        (USA, 'United States'),
    )

    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    street = models.TextField()
    city = models.CharField(max_length=DEFAULT_MAX_LENGTH, default='Austin')
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default=TX)
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES, default=USA)
    zip = models.CharField(max_length=50)

    panels = [
        FieldPanel('name'),
        MultiFieldPanel(children=[
            FieldPanel('street'),
            FieldPanel('city', classname='col5'),
            FieldPanel('state', classname='col4'),
            FieldPanel('zip', classname='col2'),
            FieldPanel('country', classname='col5'),
        ], heading='Location'),
    ]

    api_fields = [
        'name',
        'street',
        'city',
        'state',
        'country',
        'zip',
    ]

    def __str__(self):
        return self.name


class DayAndDuration(ClusterableModel):
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'
    DAY_OF_WEEK_CHOICES = (
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    )

    day_of_week = models.CharField(max_length=20, choices=DAY_OF_WEEK_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    content_panels = [
        FieldPanel('day_of_week'),
        FieldPanel('start_time'),
        FieldPanel('end_time'),
    ]

    api_fields = [
        'day_of_week',
        'start_time',
        'end_time',
    ]

    def __str__(self):
        return f'{self.day_of_week} {self.start_time} - {self.end_time}'


@register_snippet
class Contact(ClusterableModel):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    email = models.EmailField()
    phone = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    location = models.ForeignKey(Location, null=True, blank=True, related_name='+')

    api_fields = [
        'name',
        'email',
        'phone',
        'location',
        'hours',
    ]

    panels = [
        FieldPanel('name'),
        FieldPanel('email'),
        FieldPanel('phone'),
        SnippetChooserPanel('location'),
        InlinePanel('hours', label='Hours'),
    ]

    def __str__(self):
        return self.name


class ContactDayAndDuration(Orderable, DayAndDuration):
    contact = ParentalKey(Contact, related_name='hours')

    content_panels = [
        SnippetChooserPanel('day_and_duration'),
    ]


class ServicePageContact(ClusterableModel):
    page = ParentalKey(ServicePage, related_name='contacts')
    contact = models.ForeignKey(Contact, related_name='+')

    panels = [
        SnippetChooserPanel('contact'),
    ]

    api_fields = [
        'contact',
    ]

    def __str__(self):
        return self.contact.name


@register_snippet
class Department(ClusterableModel):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    mission = models.TextField()

    panels = [
        FieldPanel('name'),
        FieldPanel('mission'),
        InlinePanel('contacts', label='Contacts'),
    ]

    def __str__(self):
        return self.name


class DepartmentContact(ClusterableModel):
    department = ParentalKey(Department, related_name='contacts')
    contact = models.ForeignKey(Contact, related_name='+')

    panels = [
        SnippetChooserPanel('contact'),
    ]

    def __str__(self):
        return self.department.name

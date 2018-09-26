from django.db import models
import os
import graphene

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.utils.decorators import cached_classmethod
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
from wagtail.core.blocks import TextBlock, RichTextBlock, ListBlock, StreamBlock, StructBlock
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.snippets.models import register_snippet
from wagtail.search import index

from . import blocks as custom_blocks
from . import forms as custom_forms

WYSIWYG_GENERAL = ['h1', 'h2', 'link', 'ul', 'ol']
WYSIWYG_SERVICE_STEP = ['ul', 'ol', 'link']
DEFAULT_MAX_LENGTH = 255


class TranslatedImage(AbstractImage):
    admin_form_fields = Image.admin_form_fields

    def __str__(self):
        return self.title or self.title_en


class TranslatedImageRendition(AbstractRendition):
    image = models.ForeignKey(TranslatedImage, related_name='renditions', on_delete=models.PROTECT)

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


@register_snippet
class ThreeOneOne(ClusterableModel):
    title = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    url = models.URLField()

    def __str__(self):
        return self.title


class HomePage(Page):
    parent_page_types = []
    subpage_types = ['base.ServicePage', 'base.ProcessPage']

    image = models.ForeignKey(TranslatedImage, null=True, on_delete=models.SET_NULL, related_name='+')


class JanisPage(Page):
    parent_page_types = ['base.HomePage']
    subpage_types = []
    search_fields = Page.search_fields + [
        index.RelatedFields('owner', [
            index.SearchField('last_name', partial_match=True),
            index.FilterField('last_name'),
        ])
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(
        'base.Topic',
        on_delete=models.PROTECT,
        verbose_name='Select a Topic',
    )

    @cached_classmethod
    def get_edit_handler(cls):
        if hasattr(cls, 'edit_handler'):
            return cls.edit_handler.bind_to_model(cls)

        edit_handler = TabbedInterface([
            ObjectList([
                FieldPanel('topic'),
                FieldPanel('title')
            ] + cls.content_panels, heading='Content'),
            ObjectList(Page.promote_panels + cls.promote_panels, heading='Search Info')
        ])

        return edit_handler.bind_to_model(cls)

    def janis_url(self):
        url_page_type = self.janis_url_page_type
        page_slug = self.slug

        # TODO: Add other languages
        return os.environ["JANIS_URL"] + "/en/" + url_page_type + "/" + page_slug

    def janis_preview_url(self):
        revision = self.get_latest_revision()
        url_page_type = self.janis_url_page_type
        global_id = graphene.Node.to_global_id('PageRevisionNode', revision.id)

        return os.environ["JANIS_URL"] + "/en/preview/" + url_page_type + "/" + global_id

    class Meta:
        abstract = True

JanisPage._meta.get_field('title').verbose_name='Write an actionable title'

class ServicePage(JanisPage):
    janis_url_page_type = "services"

    steps = StreamField(
        [
            ('basic_step', RichTextBlock(
                features=WYSIWYG_SERVICE_STEP,
                label='Basic Step'
            )),
            ('step_with_options_accordian', StructBlock(
                [
                    ('options_description', TextBlock('Describe the set of options')),
                    ('options', ListBlock(
                        StructBlock([
                            ('option_name', TextBlock(
                                label='Option name. (When clicked, this name will expand the content for this option'
                            )),
                            ('option_description', RichTextBlock(
                                features=WYSIWYG_SERVICE_STEP,
                                label='Option Content',
                            )),
                        ]),
                    )),
                ],
                label="Step With Options"
            )),
        ],
        verbose_name='Write out the steps a resident needs to take to use the service',
        help_text='A step may have a basic text step or an options accordian which reveals two or more options',
        blank=True
    )

    dynamic_content = StreamField(
        [
            ('map_block', custom_blocks.SnippetChooserBlockWithAPIGoodness('base.Map', icon='site')),
            ('what_do_i_do_with_block', custom_blocks.WhatDoIDoWithBlock()),
            ('collection_schedule_block', custom_blocks.CollectionScheduleBlock()),
            ('recollect_block', custom_blocks.RecollectBlock()),
        ],
        verbose_name='Add any maps or apps that will help the resident use the service',
        blank=True
    )
    additional_content = RichTextField(
        features=WYSIWYG_GENERAL,
        verbose_name='Write any additional content describing the service',
        help_text='Section header: What else do I need to know?',
        blank=True
    )

    image = models.ForeignKey(TranslatedImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Choose an image for the service banner')

    base_form_class = custom_forms.ServicePageForm

    content_panels = [
        ImageChooserPanel('image'),
        StreamFieldPanel('steps'),
        StreamFieldPanel('dynamic_content'),
        FieldPanel('additional_content'),
        InlinePanel('contacts', label='Contacts'),
    ]

class ProcessPage(JanisPage):
    janis_url_page_type = "processes"

    description = models.TextField(blank=True)
    image = models.ForeignKey(TranslatedImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    # TODO: Add images array field

    base_form_class = custom_forms.ProcessPageForm

    content_panels = [
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
    image = models.ForeignKey(TranslatedImage, null=True, on_delete=models.SET_NULL, related_name='+')
    overview_steps = RichTextField(features=WYSIWYG_GENERAL, verbose_name='Write out the steps a resident needs to take to use the service', blank=True)
    detailed_content = RichTextField(features=WYSIWYG_GENERAL, verbose_name='Write any detailed content describing the process', blank=True)
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

@register_snippet
class Topic(ClusterableModel):
    slug = models.SlugField()
    text = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    description = models.TextField()
    call_to_action = models.TextField(blank=True)
    theme = models.ForeignKey(
        'base.Theme',
        on_delete=models.PROTECT,
        related_name='topics',
    )

    def __str__(self):
        return self.text


@register_snippet
class Theme(ClusterableModel):
    slug = models.SlugField()
    text = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    description = models.TextField()

    def __str__(self):
        return self.text


@register_snippet
class Map(ClusterableModel):
    description = models.TextField()
    location = models.ForeignKey('base.Location', on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return self.description

    def serializable_data(self):
        data = {
            'location': self.location.serializable_data(),
            'description': self.description,
        }

        data['location'].pop('pk')

        return data


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

    def __str__(self):
        return f'{self.day_of_week} {self.start_time} - {self.end_time}'


@register_snippet
class Contact(ClusterableModel):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    email = models.EmailField()
    phone = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    location = models.ForeignKey(Location, null=True, blank=True, related_name='+', on_delete=models.SET_NULL)

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


class ProcessPageContact(ClusterableModel):
    process = ParentalKey(ProcessPage, related_name='contacts')
    contact = models.ForeignKey(Contact, related_name='+', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('contact'),
    ]

    def __str__(self):
        return self.contact.name


class ServicePageContact(ClusterableModel):
    page = ParentalKey(ServicePage, related_name='contacts')
    contact = models.ForeignKey(Contact, related_name='+', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('contact'),
    ]

    def __str__(self):
        return self.contact.name


@register_snippet
class Department(ClusterableModel):
    slug = models.SlugField()
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    mission = models.TextField()
    image = models.ForeignKey(TranslatedImage, null=True, on_delete=models.SET_NULL, related_name='+')

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
    contact = models.ForeignKey(Contact, related_name='+', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('contact'),
    ]

    def __str__(self):
        return self.department.name

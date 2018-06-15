from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.snippets.models import register_snippet



from . import blocks as custom_blocks
from . import forms as custom_forms


WYSIWYG_FEATURES = ['h1', 'h2', 'link', 'ul', 'ol']
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


# Delete the source image file when an image is deleted
@receiver(post_delete, sender=TranslatedImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)


# Delete the rendition image file when a rendition is deleted
@receiver(post_delete, sender=TranslatedImage)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)


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


class ServicePage(Page):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    steps = RichTextField(features=WYSIWYG_FEATURES, verbose_name='Write out the steps a resident needs to take to use the service')
    dynamic_content = StreamField(
        [
            ('map_block', custom_blocks.SnippetChooserBlockWithAPIGoodness('base.Map', icon='site')),
            ('what_do_i_do_with_block', custom_blocks.WhatDoIDoWithBlock()),
            ('collection_schedule_block', custom_blocks.CollectionScheduleBlock()),
            ('recollect_block', custom_blocks.RecollectBlock()),
        ],
        verbose_name='Add any forms, maps, apps, or content that will help the resident use the service',
    )
    additional_content = RichTextField(features=WYSIWYG_FEATURES, verbose_name='Write any additional content describing the service', blank=True)
    topic = models.ForeignKey(
        'base.Topic',
        on_delete=models.PROTECT,
        related_name='services',
    )
    image = models.ForeignKey(TranslatedImage, null=True, on_delete=models.SET_NULL, related_name='+')

    parent_page_types = ['base.HomePage']
    subpage_types = []
    base_form_class = custom_forms.ServicePageForm

    content_panels = [
        FieldPanel('topic'),
        FieldPanel('title'),
        ImageChooserPanel('image'),
        FieldPanel('steps'),
        StreamFieldPanel('dynamic_content'),
        FieldPanel('additional_content'),
        InlinePanel('contacts', label='Contacts'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        # TODO: What should we do with the fields in settings?
        # ObjectList(Page.settings_panels, heading='Settings', classname='settings'),
    ])


class ProcessPage(Page):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    topic = models.ForeignKey(
        'base.Topic',
        on_delete=models.PROTECT,
        related_name='processes',
    )
    description = models.TextField(blank=True)
    image = models.ForeignKey(TranslatedImage, null=True, on_delete=models.SET_NULL, related_name='+')
    # TODO: Add images array field

    parent_page_types = ['base.HomePage']
    subpage_types = []
    base_form_class = custom_forms.ProcessPageForm

    content_panels = [
        FieldPanel('topic'),
        FieldPanel('title'),
        FieldPanel('description'),
        ImageChooserPanel('image'),
        InlinePanel('process_steps', label="Process steps"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        # TODO: What should we do with the fields in settings?
        # ObjectList(Page.settings_panels, heading='Settings', classname='settings'),
    ])


class ProcessPageStep(Orderable):
    page = ParentalKey(ProcessPage, related_name='process_steps')
    title = models.CharField(max_length=75)
    short_title = models.CharField(max_length=25)
    link_title = models.CharField(max_length=25)
    description = models.TextField(blank=True)
    image = models.ForeignKey(TranslatedImage, null=True, on_delete=models.SET_NULL, related_name='+')
    overview_steps = RichTextField(features=WYSIWYG_FEATURES, verbose_name='Write out the steps a resident needs to take to use the service', blank=True)
    detailed_content = RichTextField(features=WYSIWYG_FEATURES, verbose_name='Write any detailed content describing the process', blank=True)
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

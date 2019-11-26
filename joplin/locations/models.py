from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.models import Image
from wagtail.images.edit_handlers import ImageChooserPanel
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from base.models import JanisBasePage, HomePage
from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
    FieldRowPanel,
    StreamFieldPanel,
)
from base.models.translated_image import TranslatedImage
from base.models import Location as BaseLocation

# The abstract model for related links, complete with panels
from wagtail.core.fields import RichTextField, StreamField
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from base.models import JanisBasePage
from base.models.widgets import countMe, countMeTextArea, AUTHOR_LIMITS
from modelcluster.models import ClusterableModel
from base.models.constants import DEFAULT_MAX_LENGTH
from base.models.day_and_duration import DayAndDuration
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from wagtail.core import blocks


class LocationPage(JanisBasePage):
    """
    all the relevant details for a specifc location (place!?)
    decide if we want to set null or cascade
    """
    janis_url_page_type = 'location'
    alternate_name = models.CharField(max_length=255, blank=True)

    physical_street = models.CharField(max_length=255, blank=True)
    physical_unit = models.CharField(max_length=255, blank=True)
    physical_city = models.CharField(max_length=255, default='Austin', blank=True)
    physical_state = models.CharField(max_length=255, default='TX', blank=True)
    physical_country = models.CharField(max_length=255, default='USA', blank=True)
    physical_zip = models.CharField(max_length=255, blank=True)

    physical_location_photo = models.ForeignKey(
        TranslatedImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    phone_description = models.CharField(
        max_length=DEFAULT_MAX_LENGTH, blank=True)
    phone_number = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True)
    hours_exceptions = models.TextField(max_length=255, blank=True)

    mailing_street = models.CharField(max_length=255, blank=True)
    mailing_city = models.CharField(max_length=255, default='Austin', blank=True)
    mailing_state = models.CharField(max_length=255, default='TX', blank=True)
    mailing_country = models.CharField(max_length=255, default='USA', blank=True)
    mailing_zip = models.CharField(max_length=255, blank=True)

    nearest_bus_1 = models.IntegerField(blank=True)
    nearest_bus_2 = models.IntegerField(blank=True)
    nearest_bus_3 = models.IntegerField(blank=True)

    parent_page_types = ['base.HomePage', 'LocationsIndexPage']

    content_panels = [
        FieldPanel('title_en', widget=countMe),

        MultiFieldPanel(children=[
            FieldPanel('physical_street'),
            FieldPanel('physical_unit', classname='col2'),
            FieldPanel('physical_city', classname='col5'),
            FieldPanel('physical_state', classname='col4'),
            FieldPanel('physical_zip', classname='col2'),
            FieldPanel('physical_country', classname='col5'),
        ], heading='Physical Address'),
        ImageChooserPanel('physical_location_photo'),
        MultiFieldPanel(children=[
            FieldPanel('mailing_street'),
            FieldPanel('mailing_city', classname='col5'),
            FieldPanel('mailing_state', classname='col4'),
            FieldPanel('mailing_zip', classname='col2'),
            FieldPanel('mailing_country', classname='col5'),
        ],
            heading='Mailing Address',
            classname="collapsible"
        ),
        FieldPanel('alternate_name'),
        FieldRowPanel(
            children=[
                FieldPanel('phone_number', classname='col6',
                           widget=PhoneNumberInternationalFallbackWidget),
                FieldPanel('phone_description', classname='col6'),
                FieldPanel('email', classname='col6'),
            ],
            heading="Location phone"
        ),
        MultiFieldPanel(
            children=[
                InlinePanel('hours', label='Hours'),
                FieldPanel('hours_exceptions'),
            ],
            heading="Location hours"
        ),


        FieldRowPanel(
            children=[
                FieldPanel('nearest_bus_1'),
                FieldPanel('nearest_bus_2'),
                FieldPanel('nearest_bus_3'),
            ],
            heading="Nearest bus"
        ),
        InlinePanel('related_services', label='Related Services'),
    ]


class LocationDayAndDuration(Orderable, DayAndDuration):
    page = ParentalKey(LocationPage, related_name='hours')

    content_panels = [
        SnippetChooserPanel('day_and_duration'),
    ]


class DayChoiceBlock(blocks.ChoiceBlock):
    choices = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]


class AMChoiceBlock(blocks.ChoiceBlock):
    choices = [
        ('am', 'A.M.'),
        ('pm', 'P.M'),
    ]


class RecurrenceChoiceBlock(blocks.ChoiceBlock):
    choices = [
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th')
    ]


class OperatingHoursExceptionsBlock(blocks.StructBlock):
    open_or_closed = blocks.ChoiceBlock(choices=[('open', 'Open'), ('closed', 'Closed')])
    recurrence = RecurrenceChoiceBlock()
    start_time = blocks.TimeBlock()
    start_time_AM = AMChoiceBlock()
    end_time = blocks.TimeBlock()
    end_time_AM = AMChoiceBlock()


class OperatingHoursBlock(blocks.StructBlock):
    open = blocks.BooleanBlock()
    start_time = blocks.TimeBlock()
    end_time = blocks.TimeBlock()

    class Meta:
        icon = 'user'


class HoursByDay(blocks.StructBlock):
    monday = blocks.ListBlock(OperatingHoursBlock())
    tuesday = blocks.ListBlock(OperatingHoursBlock())
    wednesday = blocks.ListBlock(OperatingHoursBlock())
    thursday = blocks.ListBlock(OperatingHoursBlock())
    friday = blocks.ListBlock(OperatingHoursBlock())
    saturday = blocks.ListBlock(OperatingHoursBlock())
    sunday = blocks.ListBlock(OperatingHoursBlock())


class LocationPageRelatedServices(ClusterableModel):
    page = ParentalKey(LocationPage, related_name='related_services', default=None)
    related_service = models.ForeignKey(
        "base.servicePage",
        on_delete=models.PROTECT,
    )
    hours_by_day = StreamField([('hours', HoursByDay())], blank=True)
    exceptions = StreamField([('exceptions', OperatingHoursExceptionsBlock())], blank=True)

    panels = [
        PageChooserPanel("related_service"),
        StreamFieldPanel('hours_by_day'),
        StreamFieldPanel('exceptions'),

    ]


class LocationsIndexPage(Page):
    """
    A list of LocationPages
    """

    # Overrides the context to list all child
    # items, that are live, by the date that they were published
    # http://docs.wagtail.io/en/latest/getting_started/tutorial.html#overriding-context
    def get_context(self, request):
        context = super(LocationsIndexPage, self).get_context(request)
        context['locations'] = LocationPage.objects.descendant_of(
            self).live().order_by(
            'primary_name')
        return context


"""
maybe try this~! https://gist.github.com/pjho/f0bbcfc745989191cf305a34233388e0
"""

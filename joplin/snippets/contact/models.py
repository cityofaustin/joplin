from django.db import models

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.snippets.models import register_snippet
from wagtail.core.fields import StreamField
from wagtail.core.blocks import URLBlock
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel, FieldRowPanel, PageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.models import Orderable
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget


from base.models.constants import DEFAULT_MAX_LENGTH

@register_snippet
class Contact(ClusterableModel):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    email = models.EmailField(blank=True)
    location_page = models.ForeignKey('location_page.LocationPage', verbose_name='Select a Location', related_name='+', on_delete=models.SET_NULL, null=True, blank=True)
    hours_exceptions = models.TextField(max_length=255, blank=True)

    social_media = StreamField(
        [
            ('url', URLBlock(
                label='Social media url'
            ))
        ],
        verbose_name='Links to any social media pages',
        help_text='For example: https://www.facebook.com/atxpoliceoversight/',
        blank=True
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('email'),
        InlinePanel('phone_number', label='Phone Numbers'),
        PageChooserPanel('location_page'),
        InlinePanel('hours', label='Hours'),
        FieldPanel('hours_exceptions'),
        StreamFieldPanel('social_media'),
    ]

    def __str__(self):
        return self.name


class DayAndDuration(ClusterableModel):
    """
    creates a model to choose day of week and hourly ranges
    you can use this to define operating hours for a service or location
    """
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

    panels = [
        FieldRowPanel(
            children=[
                FieldPanel('day_of_week', classname="col5"),
                FieldPanel('start_time', classname="col3"),
                FieldPanel('end_time', classname="col3"),

            ],
            classname="full"
        ),
    ]

    def __str__(self):
        return f'{self.day_of_week} {self.start_time} - {self.end_time}'



class PhoneNumber(Orderable):
    phone_description = models.CharField(
        max_length=DEFAULT_MAX_LENGTH, blank=True)
    phone_number = PhoneNumberField()
    contact = ParentalKey(Contact, related_name='phone_number')

    content_panels = [

        FieldPanel('phone_number',
                   widget=PhoneNumberInternationalFallbackWidget),
        FieldPanel('phone_description')

    ]


class ContactDayAndDuration(Orderable, DayAndDuration):
    contact = ParentalKey(Contact, related_name='hours')

    content_panels = [
        SnippetChooserPanel('day_and_duration'),
    ]
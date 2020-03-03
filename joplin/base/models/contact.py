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

from .location import Location
from .day_and_duration import DayAndDuration

from .constants import DEFAULT_MAX_LENGTH


@register_snippet
class Contact(ClusterableModel):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    email = models.EmailField(blank=True)
    location = models.ForeignKey(
        Location, null=True, blank=True, related_name='+', on_delete=models.SET_NULL)
    location_page = models.ForeignKey('locations.LocationPage', verbose_name='Select a Location', related_name='+', on_delete=models.SET_NULL, null=True, blank=True)
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

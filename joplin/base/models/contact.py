from django.db import models

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.snippets.models import register_snippet
from wagtail.core.fields import StreamField
from wagtail.core.blocks import URLBlock
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel, FieldRowPanel
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
    email = models.EmailField()
    phone = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    location = models.ForeignKey(
        Location, null=True, blank=True, related_name='+', on_delete=models.SET_NULL)

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
        FieldPanel('phone'),
        InlinePanel('phone_number', label='Phone Numbers'),
        SnippetChooserPanel('location'),
        InlinePanel('hours', label='Hours'),
        StreamFieldPanel('social_media'),
    ]

    def __str__(self):
        return self.name


class PhoneNumber(Orderable):
    phone_description = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    phone_number = PhoneNumberField()
    contact = ParentalKey(Contact, related_name='phone_number')

    content_panels = [
        FieldRowPanel(
            [
                FieldPanel('phone_description'),
                FieldPanel('phone_number',
                           widget=PhoneNumberInternationalFallbackWidget),
            ]
        ),
    ]


class ContactDayAndDuration(Orderable, DayAndDuration):
    contact = ParentalKey(Contact, related_name='hours')

    content_panels = [
        SnippetChooserPanel('day_and_duration'),
    ]

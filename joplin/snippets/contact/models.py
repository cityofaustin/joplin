from django.db import models

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.snippets.models import register_snippet
from wagtail.core.fields import StreamField
from wagtail.core.blocks import URLBlock
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel, PageChooserPanel
from wagtail.core.models import Orderable
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from base.models.constants import DEFAULT_MAX_LENGTH


@register_snippet
class Contact(ClusterableModel):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    email = models.EmailField(blank=True)
    location_page = models.ForeignKey('location_page.LocationPage', verbose_name='Select a Location', related_name='+', on_delete=models.SET_NULL, null=True, blank=True)

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
        InlinePanel('phone_numbers', label='Phone Numbers'),
        StreamFieldPanel('social_media'),
        PageChooserPanel('location_page'),
    ]

    def __str__(self):
        return self.name


class ContactPhoneNumber(Orderable):
    phone_description = models.CharField(max_length=DEFAULT_MAX_LENGTH, blank=True)
    phone_number = PhoneNumberField()
    contact = ParentalKey(Contact, related_name='phone_numbers')

    content_panels = [
        FieldPanel('phone_number', widget=PhoneNumberInternationalFallbackWidget),
        FieldPanel('phone_description')
    ]

from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.models import Image
from wagtail.images.edit_handlers import ImageChooserPanel
from phonenumber_field.modelfields import PhoneNumberField
from base.models import JanisBasePage, HomePage
from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey
from django.contrib.admin.utils import quote
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from base.models.translated_image import TranslatedImage
from generic_chooser.widgets import AdminChooser


class Location(models.Model):
    """
    A base Django model for representing data about an
    individual location item.
    """

    full_address = models.CharField(max_length=255, blank=False)
    unit_number = models.IntegerField(blank=True)
    geography = models.CharField(max_length=255, blank=True)
    """
    optional fields to match mocks, are these really required data to store
    or should they be cosmetic/for the widget?
    street
    city
    state
    zip
    """
    # gonna need location widget that returns streetview or user selected image

    def __str__(self):
        return self.full_address


class LocationChooser(AdminChooser):
    model = Location
    choose_modal_url_name = 'location_chooser:choose'


class PhysicalAddress(Location):
    """
    inherits Location (using concrete inheritance) to add a photo for physical location
    this should also help janis know to render fields differently for this one vs mailing (see mocks)
    """
    location_photo = models.ForeignKey(
        TranslatedImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )


class LocationPageRelatedLocations(Orderable, Location):
    """
    a pattern for adding multiple related location, not currently used
    """
    page = ParentalKey(
        'locations.LocationPage',
        related_name='related_locations',
        on_delete=models.CASCADE
    )


class LocationPage(Page):
    """
    all the relevant details for a specifc location (place!?)
    decide if we want to set null or cascade
    """

    primary_name = models.CharField(max_length=255)
    alternate_name = models.CharField(max_length=255, blank=True)
    physical_address = models.OneToOneField(
        PhysicalAddress,
        blank=True,
        on_delete=models.CASCADE,
        related_name='+'
    )
    mailing_address = models.OneToOneField(
        Location,
        blank=True,
        on_delete=models.CASCADE,
        related_name='+'
    )

    parent_page_types = ['base.HomePage', 'LocationsIndexPage']

    content_panels = [
        FieldPanel('primary_name'),
        FieldPanel('alternate_name'),
        FieldPanel('physical_address', widget=LocationChooser),
        FieldPanel('mailing_address', widget=LocationChooser),
        InlinePanel('related_locations', label="Related locations"),
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

from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from phonenumber_field.modelfields import PhoneNumberField
from base.models import JanisBasePage
from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)


class Location(models.Model):
    """
    A base Django model for representing data about an
    individual location item.
    """

    full_address = models.CharField(max_length=255, blank=False)
    unit_number = models.CharField(max_length=255, blank=True)
    geography = models.CharField(max_length=255, null=True, blank=True)
    """
    optional fields to match mocks, are these really required data to store
    or should they be cosmetic/for the widget?
    street
    city
    state
    zip
    """
    address_is_physical = models.BooleanField(default=True)
    # gonna need location widget that returns streetview or user selected image
    location_photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )


class Contact(models.Model):
    """
    simple contact model w phone and email
    """
    phone_description = models.CharField(
        max_length=255, blank=True)
    phone_number = PhoneNumberField()
    email = models.EmailField(blank=True)


class LocationPageRelatedLocations(Orderable, Location):
    page = ParentalKey(
        'locations.LocationPage',
        related_name='related_locations',
        on_delete=models.CASCADE
    )


class LocationPage(JanisBasePage):
    """
    all the relevant details for a specifc location (place!?)
    """
    primary_name = models.CharField(max_length=255)
    alternate_name = models.CharField(max_length=255, blank=True)

    parent_page_types = ['LocationsIndexPage']

    content_panels = JanisBasePage.content_panels + [
        FieldPanel('primary_name'),
        FieldPanel('alternate_name'),
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

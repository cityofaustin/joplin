from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.models import Image
from wagtail.images.edit_handlers import ImageChooserPanel
from phonenumber_field.modelfields import PhoneNumberField
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
)
from base.models.translated_image import TranslatedImage
from base.models import Location as BaseLocation

# The abstract model for related links, complete with panels
from wagtail.core.fields import RichTextField
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from base.models import JanisBasePage
from base.models.widgets import countMe, countMeTextArea, AUTHOR_LIMITS
from modelcluster.models import ClusterableModel


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
            classname="collapsible collapsed"
        ),
        FieldPanel('alternate_name'),
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


class LocationPageRelatedServices(ClusterableModel):
    page = ParentalKey(LocationPage, related_name='related_services', default=None)
    related_service = models.ForeignKey(
        "base.servicePage",
        on_delete=models.PROTECT,
    )

    panels = [
        PageChooserPanel("related_service"),
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

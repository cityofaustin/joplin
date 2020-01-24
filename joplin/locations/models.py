from django.db import models
from django.core.exceptions import ValidationError
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
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, HelpPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from base.models import JanisBasePage
from base.models.widgets import countMe, countMeTextArea, AUTHOR_LIMITS
from modelcluster.models import ClusterableModel
from base.models.constants import DEFAULT_MAX_LENGTH
from base.models.day_and_duration import DayAndDuration
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from wagtail.core import blocks


def add_hours_by_day_and_exceptions(model):
    """
    here we want to add these fields to this model, but typing them all out would be super verbose
    so a little python and Django's contribute_to_class go a long way
    """
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    panels_to_add = []
    models.TextField(max_length=DEFAULT_MAX_LENGTH, blank=True).contribute_to_class(model, 'hours_exceptions')
    for day in week_days:
        day_start_field = '%s_start_time' % day.lower()
        day_end_field = '%s_end_time' % day.lower()
        models.TimeField(null=True, blank=True).contribute_to_class(model, day_start_field)
        models.TimeField(null=True, blank=True).contribute_to_class(model, day_end_field)
        models.TimeField(null=True, blank=True).contribute_to_class(model, day_start_field + "_2")
        models.TimeField(null=True, blank=True).contribute_to_class(model, day_end_field + "_2")
        panels_to_add += [

            FieldRowPanel(
                children=[

                    FieldPanel(day_start_field),
                    FieldPanel(day_end_field),
                    FieldPanel(day_start_field + "_2"),
                    FieldPanel(day_end_field + "_2"),
                ],
                heading="Hours",
            ),

        ]
    panels_to_add += [
        FieldPanel('hours_exceptions')
    ]
    panels_with_wrapper = MultiFieldPanel(children=panels_to_add, classname="collapsible hours-wrapper", heading="Location Hours")
    return panels_with_wrapper


class LocationPage(JanisBasePage):
    """
    all the relevant details for a specifc location (place!?)
    decide if we want to set null or cascade
    """
    janis_url_page_type = 'location'

    alternate_name = models.CharField(max_length=DEFAULT_MAX_LENGTH, blank=True, verbose_name="Location alternate name", help_text="Use this field if the building has a second name, or is inside a larger facility")

    physical_street = models.CharField(max_length=DEFAULT_MAX_LENGTH, blank=True, verbose_name="Street")
    physical_unit = models.CharField(max_length=DEFAULT_MAX_LENGTH, blank=True, verbose_name="Floor/Suite #")
    physical_city = models.CharField(max_length=DEFAULT_MAX_LENGTH, default='Austin', blank=True, verbose_name="City")
    physical_state = models.CharField(max_length=DEFAULT_MAX_LENGTH, default='TX', blank=True, verbose_name="State")
    physical_country = models.CharField(max_length=DEFAULT_MAX_LENGTH, default='USA', blank=True)
    physical_zip = models.CharField(max_length=DEFAULT_MAX_LENGTH, blank=True, verbose_name="ZIP")

    physical_location_photo = models.ForeignKey(
        TranslatedImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Choose a banner image",
        help_text="Use this to show an exterior of the location."
    )

    phone_description = models.CharField(
        max_length=DEFAULT_MAX_LENGTH, blank=True, verbose_name="Phone description")
    phone_number = PhoneNumberField(blank=True, verbose_name="Phone(only if location has a dedicated number)")
    email = models.EmailField(blank=True, verbose_name="Email address")

    mailing_street = models.CharField(max_length=DEFAULT_MAX_LENGTH, blank=True, verbose_name="Street or PO box")
    mailing_city = models.CharField(max_length=DEFAULT_MAX_LENGTH, default='Austin', blank=True, verbose_name="City")
    mailing_state = models.CharField(max_length=DEFAULT_MAX_LENGTH, default='TX', blank=True, verbose_name="State")
    mailing_country = models.CharField(max_length=DEFAULT_MAX_LENGTH, default='USA', blank=True)
    mailing_zip = models.CharField(max_length=DEFAULT_MAX_LENGTH, blank=True, verbose_name="ZIP")

    nearest_bus_1 = models.IntegerField(null=True, blank=True)
    nearest_bus_2 = models.IntegerField(null=True, blank=True)
    nearest_bus_3 = models.IntegerField(null=True, blank=True)

    parent_page_types = ['base.HomePage']

    content_panels = [
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),

        MultiFieldPanel(children=[
            FieldPanel('physical_street'),
            FieldPanel('physical_unit', classname='col2'),
            FieldPanel('physical_city', classname='col5'),
            FieldPanel('physical_state', classname='col4'),
            FieldPanel('physical_zip', classname='col2'),
        ], heading='Location physical address'),
        MultiFieldPanel(
            [
                HelpPanel(physical_location_photo.help_text, classname="coa-helpPanel"),
                ImageChooserPanel('physical_location_photo'),
            ],
            heading=physical_location_photo.verbose_name,
            classname='coa-multiField-nopadding'
        ),

        MultiFieldPanel(children=[
            FieldPanel('mailing_street'),
            FieldPanel('mailing_city', classname='col5'),
            FieldPanel('mailing_state', classname='col4'),
            FieldPanel('mailing_zip', classname='col2'),
        ],
            heading='Location mailing address (if applicable)',
            classname="collapsible"
        ),
        MultiFieldPanel(
            [
                HelpPanel(alternate_name.help_text, classname="coa-helpPanel"),
                FieldPanel('alternate_name'),
            ],
            heading=alternate_name.verbose_name,
            classname='coa-multiField-nopadding'
        ),

        FieldRowPanel(
            children=[
                FieldPanel('phone_number', classname='col6',
                           widget=PhoneNumberInternationalFallbackWidget),
                FieldPanel('phone_description', classname='col6'),
                FieldPanel('email', classname='col6'),
            ],
            heading="Location contact info"
        ),


        FieldRowPanel(
            children=[
                FieldPanel('nearest_bus_1'),
                FieldPanel('nearest_bus_2'),
                FieldPanel('nearest_bus_3'),
            ],
            heading="Location details"
        ),
    ]


class LocationPageRelatedServices(Orderable):

    page = ParentalKey(LocationPage, related_name='related_services', default=None)
    related_service = models.ForeignKey(
        "base.servicePage",
        on_delete=models.PROTECT,
    )
    hours_same_as_location = models.BooleanField(default=False, verbose_name="The hours for this service are the same as the location hours")

    # slightly clever property + filter for model clean function
    @property
    def all_hours_fields(self):
        return [field for field in self._meta.fields if field.get_internal_type() == 'TimeField']

    def clean(self):
        if self.hours_same_as_location is False and not any((getattr(self, field.name) for field in self.all_hours_fields)):
            raise ValidationError({'hours_same_as_location': ('Please either check this or input hours for this service')})

    panels = [
        PageChooserPanel("related_service"),
        FieldPanel("hours_same_as_location"),

    ]


LocationPageRelatedServices.panels += [add_hours_by_day_and_exceptions(LocationPageRelatedServices)]
LocationPage.content_panels += [add_hours_by_day_and_exceptions(LocationPage), InlinePanel('related_services', label='Related Services'), ]
# override title field to change verbose name
# NOTE: this may break/cause problems if we ever make JanisBasePage NOT absctract
# commenting out for now since this is making *every* content type have the field name Location name
# the problem seems to be that title comes from the wagtail Page model, and is not absctract.
# we then inherit that non abstract model with janisbasepage which IS abstract, then this page inherits that and is NOT abstract
# LocationPage._meta.get_field('title').verbose_name = 'Location name'

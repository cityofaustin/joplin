from django.db import models
from django.utils import translation
from wagtail.core.blocks import StructBlock, PageChooserBlock, TextBlock
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    InlinePanel,
    FieldRowPanel,
    StreamFieldPanel,
    MultiFieldPanel,
)

from pages.location_page.models import LocationPage
from pages.information_page.models import InformationPage
from pages.service_page.models import ServicePage
from snippets.contact.models import Contact
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import StreamBlock
from wagtail.core.models import Orderable
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, HelpPanel
from base.forms import EventPageForm
from pages.base_page.models import JanisBasePage
from base.models.widgets import countMe, AUTHOR_LIMITS
from base.models.constants import DEFAULT_MAX_LENGTH, WYSIWYG_GENERAL
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from publish_preflight.requirements import FieldPublishRequirement, StreamFieldPublishRequirement


def only_one_physical_location(stream_value):
    """
    Streamfield requirement
    :param stream_value:
    Checks to see that the stream_value has length and if there are two locations that one of them is a virtual event
    Events cannot have two physical locations
    """
    if not stream_value:
        return False
    if len(stream_value) > 0:
        if len(stream_value.stream_data) == 2:
            loc1 = stream_value.stream_data[0][0]
            loc2 = stream_value.stream_data[1][0]
            return loc1 == 'virtual_event' or loc2 == 'virtual_event'
        return True
    return False


class EventPage(JanisBasePage):
    janis_url_page_type = 'event'

    description = RichTextField(
        features=WYSIWYG_GENERAL,
        verbose_name='Description',
        help_text='Include any information people need to know, such as meeting agenda.',
        blank=True
    )

    date = models.DateField(verbose_name="Event date", blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    location_blocks = StreamField(
        StreamBlock(
            [
                ('city_of_Austin_location', StructBlock(
                    [
                        ('location_page', PageChooserBlock(label="Location", page_type=[LocationPage], classname='do-not-hide')),
                        ('additional_details_en', TextBlock(label='Any other necessary location details, such as room number [en]', required=False)),
                        ('additional_details_es', TextBlock(label='Any other necessary location details, such as room number [es]', required=False)),
                        ('additional_details_ar', TextBlock(label='Any other necessary location details, such as room number [ar]', required=False)),
                        ('additional_details_vi', TextBlock(label='Any other necessary location details, such as room number [vi]', required=False)),
                    ]
                )),
                ('remote_(non_COA)_location', StructBlock(
                    [
                        ('name_en', TextBlock(label='Name of venue [en]')),
                        ('name_es', TextBlock(label='Name of venue [es]', required=False)),
                        ('name_ar', TextBlock(label='Name of venue [ar]', required=False)),
                        ('name_vi', TextBlock(label='Name of venue [vi]', required=False)),
                        ('street', TextBlock(label='Street', required=False)),
                        ('unit', TextBlock(label='Unit', required=False)),
                        ('city', TextBlock(label='City', required=False)),
                        ('state', TextBlock(label='State', required=False)),
                        ('zip', TextBlock(label='ZIP', required=False)),
                        ('additional_details_en', TextBlock(label='Any other necessary location details, such as room number [en]', required=False)),
                        ('additional_details_es', TextBlock(label='Any other necessary location details, such as room number [es]', required=False)),
                        ('additional_details_ar', TextBlock(label='Any other necessary location details, such as room number [ar]', required=False)),
                        ('additional_details_vi', TextBlock(label='Any other necessary location details, such as room number [vi]', required=False)),
                    ],
                )),
                ('virtual_event', StructBlock(
                    [
                        ('event_link', TextBlock(label='Event link or location')),
                        ('additional_information_en', TextBlock(label='Any other necessary information, such as '
                                                                      'meeting code [en]', required=False)),
                        ('additional_information_es', TextBlock(label='Any other necessary information, such as '
                                                                      'meeting code [es]', required=False)),
                        ('additional_information_ar', TextBlock(label='Any other necessary information, such as '
                                                                      'meeting code [ar]', required=False)),
                        ('additional_information_vi', TextBlock(label='Any other necessary information, such as '
                                                                      'meeting code [vi]', required=False)),
                    ]))
            ],
            verbose_name='Add location of event',
            blank=True,
            max_num=2,
        )
    )

    event_is_free = models.BooleanField(verbose_name="This event is free", default=True)

    registration_url = models.URLField(
        verbose_name='Registration',
        help_text='The URL where the resident may register for the event, if needed',
        blank=True
    )

    contact = models.ForeignKey(Contact, related_name='+', blank=True, null=True, on_delete=models.SET_NULL)

    canceled = models.BooleanField(
        verbose_name="Cancel this event",
        help_text="Canceling an event will not unpublish it, but it will display the event as canceled.",
        default=False
    )

    base_form_class = EventPageForm

    @property
    def fees_range(self):
        fees = self.fees.values_list('fee')
        if fees:
            formatted_fees = []
            for f in fees:
                f = f[0]
                if f%1 == 0:
                    # If fee is a whole dollar amount, remove trailing .00 cents
                    f = f.to_integral()
                f = f.to_eng_string()
                formatted_fees.append("$" + f)
            formatted_fees.sort()
            if len(formatted_fees) >= 2:
                return formatted_fees[0] + '-' + formatted_fees[-1]
            else:
                return formatted_fees[0]
        elif self.event_is_free:
            return ""
        return ""

    # Get the name of the first location, for use in search results
    @property
    def location_name(self):
        locations = self.location_blocks.stream_data
        if locations:
            location = locations[0]
            location_value = location['value']
            location_type = location['type']

            if location_type == "remote_location":
                english_name = location_value['name_en']
                if translation.get_language() == 'en':
                    return english_name
                elif translation.get_language() == 'es':
                    return location_value['name_es'] or english_name
            elif location_type == "city_location":
                return LocationPage.objects.get(id=location_value['location_page']).title
        return ""

    @property
    def search_output(self):
        output = {}
        output.update(super().search_output)
        output.update({
            "date": self.date and self.date.isoformat(),
            "startTime": self.start_time and self.start_time.isoformat(),
            "endTime": self.end_time and self.end_time.isoformat(),
            "eventIsFree": self.event_is_free,
            "registrationUrl": self.registration_url,
            "locationName": self.location_name,
            "eventUrl": self.janis_urls()[0],
            "feesRange": self.fees_range,
        })
        return output

    publish_requirements = (
        FieldPublishRequirement("description", message="Description is required.", langs=["en"]),
        FieldPublishRequirement("date", message="Date is required."),
        FieldPublishRequirement("start_time", message="Start time is required."),
        StreamFieldPublishRequirement("location_blocks", message="Please select one physical location or one physical "
                                                                 "location and one virtual location",
                                      criteria=only_one_physical_location),
    )

    content_panels = [
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('slug_en'),
        FieldPanel('slug_es'),
        FieldPanel('slug_ar'),
        FieldPanel('slug_vi'),
        MultiFieldPanel(
            [
                HelpPanel(description.help_text, classname="coa-helpPanel"),
                FieldPanel('description'),
            ],
            heading=description.verbose_name,
            classname='coa-multiField-nopadding'
        ),
        FieldPanel('date'),
        FieldRowPanel(
            children=[
                FieldPanel('start_time', classname='col3'),
                FieldPanel('end_time', classname='col3'),
            ],
            heading="Event time",
        ),
        StreamFieldPanel('location_blocks'),
        FieldPanel('event_is_free'),
        InlinePanel('fees', label='Fees', classname='coa-eventFees'),
        MultiFieldPanel(
            [
                HelpPanel(registration_url.help_text, classname="coa-helpPanel"),
                FieldPanel('registration_url'),
            ],
            heading=registration_url.verbose_name,
            classname='coa-multiField-nopadding'
        ),
        InlinePanel('related_page', heading='Select the page(s) where this event should display', label='Page',
                    help_text='Add links to Service, Information, or Location Pages',
                    min_num=None),
        SnippetChooserPanel('contact'),
        MultiFieldPanel(
            [
                HelpPanel(canceled.help_text, classname="coa-helpPanel"),
                FieldPanel('canceled'),
            ],
            heading=canceled.verbose_name,
            classname='coa-multiField-nopadding'
        ),
    ]

    def janis_urls(self):
        # Should publish at event/<fullYear>/<month>/<day>/<slug>"
        # Example: event/2020/4/10/event-1
        if self.slug and self.date and self.date.year and self.date.month and self.date.day:
            return [f'/{self.janis_url_page_type}/{self.date.year}/{self.date.month}/{self.date.day}/{self.slug_en}']
        return []


class EventPageFee(Orderable):
    page = ParentalKey(EventPage, related_name='fees', default=None)
    fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    fee_label = models.CharField(blank=True, verbose_name='Label (kids, adults, seniors, etc.)', max_length=DEFAULT_MAX_LENGTH)

    panels = [
        FieldRowPanel(
            children=[
                FieldPanel('fee', classname='col3'),
                FieldPanel('fee_label', classname='col9'),
            ],
        ),
    ]


class EventPageRelatedPage(Orderable):
    event = ParentalKey(EventPage, related_name='related_page', default=None)
    page = models.ForeignKey('wagtailcore.Page', verbose_name='Page where event is displayed',
                             related_name='+', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('page', page_type=[InformationPage, ServicePage, LocationPage]),
    ]

    def __str__(self):
        return self.page.title

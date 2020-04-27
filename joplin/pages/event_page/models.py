from django.db import models
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


class EventPage(JanisBasePage):
    janis_url_page_type = 'event'

    description = RichTextField(
        features=WYSIWYG_GENERAL,
        verbose_name='Description',
        help_text='Full description of the event',
        blank=True
    )

    date = models.DateField(verbose_name="Event date", blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    location_blocks = StreamField(
        StreamBlock(
            [
                ('city_location', StructBlock(
                    [
                        ('location_page', PageChooserBlock(label="Location", page_type=[LocationPage], classname='do-not-hide')),
                        ('additional_details_en', TextBlock(label='Any other necessary location details, such as room number [en]', required=False)),
                        ('additional_details_es', TextBlock(label='Any other necessary location details, such as room number [es]', required=False)),
                        ('additional_details_ar', TextBlock(label='Any other necessary location details, such as room number [ar]', required=False)),
                        ('additional_details_vi', TextBlock(label='Any other necessary location details, such as room number [vi]', required=False)),
                    ]
                )),
                ('remote_location', StructBlock(
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
            ],
            verbose_name='Add location of event',
            blank=True,
            max_num=1,
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

    publish_requirements = (
        FieldPublishRequirement("description", message="Description is required.", langs=["en"]),
        FieldPublishRequirement("date", message="Date is required."),
        FieldPublishRequirement("start_time", message="Start time is required."),
        StreamFieldPublishRequirement("location_blocks", message="Location is required."),
    )

    content_panels = [
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
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
                    help_text='Add links to Service or Information Pages',
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
            return [f'/{self.janis_url_page_type}/{self.date.year}/{self.date.month}/{self.date.day}/{self.slug}']
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

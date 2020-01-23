from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.models import Image
from wagtail.images.edit_handlers import ImageChooserPanel
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from base.models import JanisBasePage, HomePage
from wagtail.core.models import Page, Orderable
from wagtail.core.blocks import StructBlock, PageChooserBlock, TextBlock
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
from locations.models import LocationPage

# The abstract model for related links, complete with panels
from wagtail.core.fields import RichTextField, StreamField
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, HelpPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from base.models import JanisBasePage
from base.models.widgets import countMe, countMeLongTextArea, AUTHOR_LIMITS
from modelcluster.models import ClusterableModel
from base.models.constants import DEFAULT_MAX_LENGTH
from base.models.day_and_duration import DayAndDuration
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from wagtail.core import blocks


class EventPage(JanisBasePage):
    janis_url_page_type = 'event'

    description = models.TextField(blank=True, verbose_name='Full description of the event')
    
    date = models.DateField(verbose_name="Event date", blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    location_blocks = StreamField(
        [
            ('city_location', StructBlock(
                [
                    ('location_page', PageChooserBlock(label="Location", page_type=[LocationPage], classname='do-not-hide')),
                    ('additional_details_en', TextBlock(label='Any other necessary location details, such as room number [en]')),
                    ('additional_details_es', TextBlock(label='Any other necessary location details, such as room number [es]', required=False)),
                    ('additional_details_ar', TextBlock(label='Any other necessary location details, such as room number [ar]', required=False)),
                    ('additional_details_vi', TextBlock(label='Any other necessary location details, such as room number [vi]', required=False)),
                ]
            )),
            ('remote_location', StructBlock(
                [
                    ('street', TextBlock(label='Street')),
                    ('unit', TextBlock(label='Unit')),
                    ('city', TextBlock(label='City')),
                    ('state', TextBlock(label='State')),
                    ('country', TextBlock(label='Country')),
                    ('zip', TextBlock(label='ZIP')),
                    ('additional_details_en', TextBlock(label='Any other necessary location details, such as room number [en]')),
                    ('additional_details_es', TextBlock(label='Any other necessary location details, such as room number [es]', required=False)),
                    ('additional_details_ar', TextBlock(label='Any other necessary location details, such as room number [ar]', required=False)),
                    ('additional_details_vi', TextBlock(label='Any other necessary location details, such as room number [vi]', required=False)),
                ],
                # label="Step With Options"
            )),
        ],
        verbose_name='Add location of event',
        # this gets called in the help panel
        # help_text='A step may have a basic text step or an options accordion which reveals two or more options',
        blank=True
    )

    content_panels = [
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('description', widget=countMeLongTextArea),
        FieldPanel('date'),
        FieldRowPanel(
            children=[
                FieldPanel('start_time', classname='col3'),
                FieldPanel('end_time', classname='col3'),
            ],
            heading="Event time",
        ),
        StreamFieldPanel('location_blocks')


    ]

    parent_page_types = ['base.HomePage']

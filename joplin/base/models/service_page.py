from django.db import models

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import ListBlock, RichTextBlock, StructBlock, TextBlock, PageChooserBlock
from wagtail.admin.edit_handlers import FieldPanel, HelpPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from base.blocks import SnippetChooserBlockWithAPIGoodness, WhatDoIDoWithBlock, CollectionScheduleBlock, RecollectBlock
from base.forms import ServicePageForm

from .janis_page import JanisBasePage
from locations.models import LocationPage
from .contact import Contact

from .constants import WYSIWYG_GENERAL, SHORT_DESCRIPTION_LENGTH
from .widgets import countMe, countMeTextArea

from publish_preflight.requirements import FieldPublishRequirement, StreamFieldPublishRequirement, ConditionalPublishRequirement, RelationPublishRequirement


WYSIWYG_SERVICE_STEP = ['ul', 'link', 'code', 'rich-text-button-link', 'document-link']


class ServicePage(JanisBasePage):
    janis_url_page_type = "services"

    steps = StreamField(
        [
            ('basic_step', RichTextBlock(
                features=WYSIWYG_SERVICE_STEP,
                label='Basic Step'
            )),
            ('step_with_options_accordian', StructBlock(
                [
                    ('options_description', RichTextBlock(
                        features=WYSIWYG_SERVICE_STEP,
                        # richTextPlaceholder.js searches for the class 'coa-option-description' and replaces placeholder text
                        # The placeholder text is not part of the richtext input, but rather a div mask.
                        classname='coa-option-description',
                    )),
                    ('options', ListBlock(
                        StructBlock([
                            ('option_name', TextBlock(
                                label='Option name. (When clicked, this name will expand the content for this option'
                            )),
                            ('option_description', RichTextBlock(
                                features=WYSIWYG_SERVICE_STEP,
                                label='Option Content',
                            )),
                        ]),
                    )),
                ],
                label="Step With Options"
            )),
            ('step_with_locations', StructBlock(
                [
                    ('locations_description', RichTextBlock(
                        features=WYSIWYG_SERVICE_STEP,
                        # richTextPlaceholder.js searches for the class 'coa-option-description' and replaces placeholder text
                        # The placeholder text is not part of the richtext input, but rather a div mask.
                        classname='coa-locations-description',
                    )),
                    ('locations', ListBlock(PageChooserBlock(label="Location", page_type=[LocationPage]))),
                ],
                label="Step with locations"
            )),


        ],
        verbose_name='Write out the steps a resident needs to take to use the service',
        # this gets called in the help panel
        help_text='A step may have a basic text step or an options accordion which reveals two or more options',
        blank=True
    )

    dynamic_content = StreamField(
        [
            ('map_block', SnippetChooserBlockWithAPIGoodness('base.Map', icon='site')),
            ('what_do_i_do_with_block', WhatDoIDoWithBlock()),
            ('collection_schedule_block', CollectionScheduleBlock()),
            ('recollect_block', RecollectBlock()),
        ],
        verbose_name='Add any maps or apps that will help the resident use the service',
        blank=True
    )
    additional_content = RichTextField(
        features=WYSIWYG_GENERAL,
        verbose_name='Write any additional content describing the service',
        help_text='Section header: What else do I need to know?',
        blank=True
    )

    base_form_class = ServicePageForm

    short_description = models.TextField(
        max_length=SHORT_DESCRIPTION_LENGTH,
        blank=True,
        verbose_name='Write a description of this service'
    )

    publish_requirements = (
        FieldPublishRequirement("short_description", message="A description is required", langs=["en"]),
        StreamFieldPublishRequirement("steps", langs=["en"]),
        ConditionalPublishRequirement(
            RelationPublishRequirement("topics"),
            "or",
            ConditionalPublishRequirement(
                RelationPublishRequirement("related_departments"),
                "or",
                FieldPublishRequirement("coa_global"),
            ),
            message="You must have at least 1 topic or 1 department or 'Top Level' checked."
        ),
    )

    content_panels = [
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('short_description', widget=countMeTextArea),
        InlinePanel('topics', label='Topics'),
        InlinePanel('related_departments', label='Related Departments'),
        MultiFieldPanel(
            [
                HelpPanel(steps.help_text, classname="coa-helpPanel"),
                StreamFieldPanel('steps')
            ],
            heading=steps.verbose_name,
            classname='coa-multiField-nopadding'
        ),
        StreamFieldPanel('dynamic_content'),
        MultiFieldPanel(
            [
                HelpPanel(additional_content.help_text,
                          classname="coa-helpPanel"),
                FieldPanel('additional_content')
            ],
            heading=additional_content.verbose_name,
            classname='coa-multiField-nopadding'
        ),
        InlinePanel('contacts', label='Contacts', max_num=1),
    ]


class ServicePageTopic(ClusterableModel):
    page = ParentalKey(ServicePage, related_name='topics')
    topic = models.ForeignKey('base.TopicPage', verbose_name='Select a Topic', related_name='+', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('topic'),
    ]


class ServicePageContact(ClusterableModel):
    page = ParentalKey(ServicePage, related_name='contacts')
    contact = models.ForeignKey(
        Contact, related_name='+', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('contact'),
    ]

    def __str__(self):
        return self.contact.name


class ServicePageRelatedDepartments(ClusterableModel):
    page = ParentalKey(
        ServicePage, related_name='related_departments', default=None)
    related_department = models.ForeignKey(
        "base.departmentPage",
        on_delete=models.PROTECT,
    )

    panels = [
        # Use a SnippetChooserPanel because blog.BlogAuthor is registered as a snippet
        PageChooserPanel("related_department"),
    ]

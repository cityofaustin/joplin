from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import RichTextBlock
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from base.forms import InformationPageForm

from .janis_page import JanisBasePage, AdminOnlyFieldPanel
from .contact import Contact

from .constants import WYSIWYG_GENERAL
from .widgets import countMe, countMeTextArea, AUTHOR_LIMITS
from countable_field import widgets


class InformationPage(JanisBasePage):
    janis_url_page_type = "information"

    description = models.TextField(blank=True, verbose_name='Write a description of this page')

    coaGlobal = models.BooleanField(default=False, verbose_name='Make this a top level page')

    options = StreamField(
        [
            ('option', RichTextBlock(
                features=WYSIWYG_GENERAL,
                label='Option'
            ))
        ],
        verbose_name='Add option sections as needed.',
        help_text='Options are needed when the reader needs to make a choice between a few options, such as ways to fill out a form (online, by phone, in person, etc.).',
        blank=True
    )

    additional_content = RichTextField(
        features=WYSIWYG_GENERAL,
        verbose_name='Write any additional content describing the service',
        blank=True
    )

    # TODO: Add images array field

    base_form_class = InformationPageForm

    content_panels = [
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        AdminOnlyFieldPanel('coaGlobal', classname="admin-only-field"),
        InlinePanel('topics', label='Topics'),
        InlinePanel('related_departments', label='Related Departments'),
        FieldPanel('description', widget=countMeTextArea),
        StreamFieldPanel('options'),
        FieldPanel('additional_content'),
        InlinePanel('contacts', label='Contacts'),
    ]


class InformationPageRelatedDepartments(ClusterableModel):
    page = ParentalKey(InformationPage, related_name='related_departments', default=None)
    related_department = models.ForeignKey(
        "base.departmentPage",
        on_delete=models.PROTECT,
    )

    panels = [
        # Use a SnippetChooserPanel because blog.BlogAuthor is registered as a snippet
        PageChooserPanel("related_department"),
    ]


class InformationPageContact(ClusterableModel):
    page = ParentalKey(InformationPage, related_name='contacts')
    contact = models.ForeignKey(Contact, related_name='+', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('contact'),
    ]

    def __str__(self):
        return self.contact.name


class InformationPageTopic(ClusterableModel):
    page = ParentalKey(InformationPage, related_name='topics')
    topic = models.ForeignKey('base.TopicPage', verbose_name='Select a Topic', related_name='+', on_delete=models.CASCADE)
    toplink = models.BooleanField(default=False, verbose_name='Make this page a top link for this topic')

    panels = [
        MultiFieldPanel(
            [
                PageChooserPanel('topic'),
                FieldPanel('toplink'),
            ]
        ),
    ]

    def __str__(self):
        return self.topic.text

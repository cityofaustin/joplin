from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import RichTextBlock
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from base.forms import InformationPageForm

from pages.base_page.models import JanisBasePage
from base.models.contact import Contact

from base.models.constants import WYSIWYG_GENERAL
from base.models.widgets import countMe, countMeTextArea
from countable_field import widgets

from publish_preflight.requirements import FieldPublishRequirement, RelationPublishRequirement, ConditionalPublishRequirement, DepartmentPublishRequirement

from pages.topic_page.models import JanisBasePageWithTopics


class InformationPage(JanisBasePageWithTopics):
    """
    Basic page model primarly for providing informational content
    """
    janis_url_page_type = "information"

    description = models.TextField(blank=True, verbose_name='Write a description of this page')
    # TODO: remove options? They don't appear to be used in info pages anymore
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

    publish_requirements = (
        FieldPublishRequirement("description", langs=["en"], message="You need to write a description before publishing"),
        FieldPublishRequirement("additional_content", langs=["en"], message="You need to write additional content in order to publish"),
        ConditionalPublishRequirement(
            RelationPublishRequirement("topics"),
            "or",
            ConditionalPublishRequirement(
                DepartmentPublishRequirement(),
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
        InlinePanel('topics', label='Topics'),
        FieldPanel('description', widget=countMeTextArea),
        # hidden for now, see: https://austininnovation.slack.com/archives/C8T4YD23T/p1570659780017500?thread_ts=1570659723.017100&cid=C8T4YD23T
        # StreamFieldPanel('options'),
        FieldPanel('additional_content'),
        InlinePanel('contacts', label='Contacts'),
    ]


class InformationPageContact(ClusterableModel):
    page = ParentalKey(InformationPage, related_name='contacts')
    contact = models.ForeignKey(Contact, related_name='+', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('contact'),
    ]

    def __str__(self):
        return self.contact.name
from django.db import models

from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from base.forms import InformationPageForm

from snippets.contact.models import Contact

from base.models.constants import WYSIWYG_GENERAL_IMAGE
from base.models.widgets import countMe, countMeTextArea

from publish_preflight.requirements import FieldPublishRequirement, RelationPublishRequirement, ConditionalPublishRequirement, DepartmentPublishRequirement

from pages.topic_page.models import JanisBasePageWithTopics


class InformationPage(JanisBasePageWithTopics):
    """
    Basic page model primarily for providing informational content
    """
    janis_url_page_type = "information"

    description = models.TextField(blank=True, verbose_name='Write a description of this page')

    additional_content = RichTextField(
        features=WYSIWYG_GENERAL_IMAGE,
        verbose_name='Write any additional content describing the service',
        blank=True
    )

    contact = models.ForeignKey(Contact, related_name='+', blank=True, null=True, on_delete=models.SET_NULL)

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
        FieldPanel('slug_en'),
        FieldPanel('slug_es'),
        FieldPanel('slug_ar'),
        FieldPanel('slug_vi'),
        InlinePanel('topics', label='Topics'),
        FieldPanel('description', widget=countMeTextArea),
        # hidden for now, see: https://austininnovation.slack.com/archives/C8T4YD23T/p1570659780017500?thread_ts=1570659723.017100&cid=C8T4YD23T
        # StreamFieldPanel('options'),
        FieldPanel('additional_content'),
        SnippetChooserPanel('contact'),
    ]

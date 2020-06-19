from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel

from pages.topic_page.models import JanisBasePageWithTopics
from base.forms import OfficialDocumentListForm
from base.models.widgets import countMeTextArea
from publish_preflight.requirements import FieldPublishRequirement, RelationPublishRequirement, \
     ConditionalPublishRequirement, DepartmentPublishRequirement


"""
This is a page that displays a list of Official Documents (model: OfficialDocumentPage).
The relationship is similar to that of topic collection and topic page.
This page can be assigned to multiple topics or departments.
The Documents will be displayed in date descending order (newest first by the "date" field).
"""


class OfficialDocumentList(JanisBasePageWithTopics):
    janis_url_page_type = "official_document_list"
    base_form_class = OfficialDocumentListForm

    description = models.TextField(blank=True)

    publish_requirements = (
        FieldPublishRequirement("description", langs=["en"],
                                message="You need to write a description before publishing"),
        ConditionalPublishRequirement(
            RelationPublishRequirement("topics"),
            "or",
            DepartmentPublishRequirement(),
            message="You must have at least 1 topic or 1 department selected.",
        )
    )

    content_panels = [
        FieldPanel('description', widget=countMeTextArea),
        InlinePanel('topics', label='Topics'),
    ]

from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel

from pages.topic_page.models import JanisBasePageWithTopics
from base.forms import OfficialDocumentCollectionForm
from base.models.widgets import countMeTextArea, countMe
from publish_preflight.requirements import FieldPublishRequirement, RelationPublishRequirement, \
     ConditionalPublishRequirement, DepartmentPublishRequirement


"""
This is a page that displays a list of Official Documents (model: OfficialDocumentPage).
The relationship is similar to that of topic collection and topic page.
This page can be assigned to multiple topics or departments.
The Documents will be displayed in date descending order (newest first by the "date" field).
"""


class OfficialDocumentCollection(JanisBasePageWithTopics):
    janis_url_page_type = "official_document_collection"
    base_form_class = OfficialDocumentCollectionForm

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
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('slug_en'),
        FieldPanel('slug_es'),
        FieldPanel('slug_ar'),
        FieldPanel('slug_vi'),
        FieldPanel('description', widget=countMeTextArea),
        InlinePanel('topics', label='Topics'),
    ]

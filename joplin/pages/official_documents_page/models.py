from django.db import models

from modelcluster.fields import ParentalKey

from base.forms import OfficialDocumentPageForm, OfficialDocumentPageOldForm

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.core.models import Orderable
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel

from pages.base_page.models import JanisBasePage

from base.models.constants import DEFAULT_MAX_LENGTH
from base.models.widgets import countMe, countMeTextArea, AUTHOR_LIMITS
from countable_field import widgets
from publish_preflight.requirements import FieldPublishRequirement, RelationPublishRequirement, \
    ConditionalPublishRequirement, DepartmentPublishRequirement

from pages.topic_page.models import JanisBasePageWithTopics

"""
This is a page that displays a list of Official Documents (model: DocumentPageOfficialDocument).
This page can be assigned to multiple topics or departments.
The Documents will be displayed in date descending order (newest first by the "date" field).
Eventually the OfficialDocumentPageOfficialDocument should be replaced by a model using Wagtail Documents
"""


class OfficialDocumentPageOld(JanisBasePageWithTopics):
    janis_url_page_type = "official_document"
    base_form_class = OfficialDocumentPageOldForm

    description = models.TextField(blank=True)

    publish_requirements = (
        FieldPublishRequirement("description", langs=["en"],
                                message="You need to write a description before publishing"),
        RelationPublishRequirement('documents'),
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
        InlinePanel('documents', label="Documents",
                    heading="Entries will be listed by document date (newest first)."),
    ]


"""
An OfficialDocumentPageDocument is a Document belonging to a single OfficialDocumentPage.
One OfficialDocumentPage can have many OfficialDocumentPageDocuments.
"""


class OfficialDocumentPageDocument(Orderable):
    page = ParentalKey(OfficialDocumentPageOld, related_name='documents')
    date = models.DateField(verbose_name="Document date", null=True)
    title = models.CharField(verbose_name="Document title", max_length=DEFAULT_MAX_LENGTH)
    authoring_office = models.CharField(verbose_name="Authoring office of document", max_length=DEFAULT_MAX_LENGTH)
    summary = models.TextField(verbose_name="Document summary")
    name = models.CharField(verbose_name="Name of Document", max_length=DEFAULT_MAX_LENGTH)
    document = models.ForeignKey(Document, null=True, blank=False, on_delete=models.SET_NULL, related_name='+',
                                 verbose_name="Document [en]")
    document_es = models.ForeignKey(Document, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
                                    verbose_name="Document [es]")

    panels = [
        FieldPanel('date'),
        FieldPanel('title', widget=countMe),
        FieldPanel('authoring_office', widget=countMe),
        FieldPanel('summary', widget=widgets.CountableWidget(attrs={
            'data-count': 'characters',
            'data-max-count': AUTHOR_LIMITS['document_summary'],
            'data-count-direction': 'down'
        })),
        FieldPanel('name', widget=countMe),
        DocumentChooserPanel('document'),
        DocumentChooserPanel('document_es')
    ]

    class Meta:
        indexes = [models.Index(fields=['-date'])]


class OfficialDocumentPage(JanisBasePage):
    janis_url_page_type = "official_document_page"
    base_form_class = OfficialDocumentPageForm

    date = models.DateField(verbose_name="Document date", null=True, blank=True)
    authoring_office = models.CharField(verbose_name="Authoring office of document", max_length=DEFAULT_MAX_LENGTH,
                                        blank=True)
    summary = models.TextField(verbose_name="Document summary", blank=True)
    name = models.CharField(verbose_name="Name of Document", max_length=DEFAULT_MAX_LENGTH, blank=True)
    document = models.ForeignKey(Document, null=True, blank=True, on_delete=models.SET_NULL, related_name='+',
                                 verbose_name="Document [en]")
    document_es = models.ForeignKey(Document, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
                                    verbose_name="Document [es]")

    publish_requirements = (
        FieldPublishRequirement("date",
                                message="You need to include a date before publishing"),
        FieldPublishRequirement("authoring_office", langs=["en"],
                                message="You need to include the authoring office before publishing"),
        FieldPublishRequirement("summary", langs=["en"],
                                message="You need to include a summary before publishing"),
        FieldPublishRequirement("name", langs=["en"],
                                message="You need to include a name before publishing"),
        FieldPublishRequirement('document'),
        RelationPublishRequirement('official_document_collection'),
    )

    content_panels = [
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('date'),
        FieldPanel('authoring_office', widget=countMe),
        FieldPanel('summary', widget=widgets.CountableWidget(attrs={
            'data-count': 'characters',
            'data-max-count': AUTHOR_LIMITS['document_summary'],
            'data-count-direction': 'down'
        })),
        FieldPanel('name', widget=countMe),
        DocumentChooserPanel('document'),
        DocumentChooserPanel('document_es'),
        # InlinePanel('official_document_collection', label="Official Document Collections this Document belongs to")
    ]

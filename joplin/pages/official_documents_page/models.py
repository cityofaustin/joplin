from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from base.forms import OfficialDocumentPageForm

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel

from pages.base_page.models import JanisBasePage

from base.models.constants import DEFAULT_MAX_LENGTH
from base.models.widgets import countMe, AUTHOR_LIMITS
from countable_field import widgets
from publish_preflight.requirements import FieldPublishRequirement, RelationPublishRequirement


class OfficialDocumentPage(JanisBasePage):
    janis_url_page_type = "official_document_page"
    base_form_class = OfficialDocumentPageForm

    date = models.DateField(verbose_name="Document date", null=True, blank=True)
    authoring_office = models.CharField(verbose_name="Authoring office of document", max_length=DEFAULT_MAX_LENGTH,
                                        blank=True)
    summary = models.TextField(verbose_name="Document summary", blank=True)
    body = models.TextField(verbose_name="Document text", blank=True)
    name = models.CharField(verbose_name="Name of Document", max_length=DEFAULT_MAX_LENGTH, blank=True)
    document = models.ForeignKey(Document, null=True, blank=True, on_delete=models.SET_NULL, related_name='+',
                                 verbose_name="Document [en]")
    document_es = models.ForeignKey(Document, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
                                    verbose_name="Document [es]")

    @property
    def search_summary(self):
        return self.summary

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
        FieldPanel('slug_en'),
        FieldPanel('slug_es'),
        FieldPanel('slug_ar'),
        FieldPanel('slug_vi'),
        FieldPanel('date'),
        FieldPanel('authoring_office', widget=countMe),
        FieldPanel('summary', widget=widgets.CountableWidget(attrs={
            'data-count': 'characters',
            'data-max-count': AUTHOR_LIMITS['document_summary'],
            'data-count-direction': 'down'
        })),
        FieldPanel('body'),
        FieldPanel('name', widget=countMe),
        DocumentChooserPanel('document'),
        DocumentChooserPanel('document_es'),
        InlinePanel('official_document_collection', label="Official document collections this document belongs to"),
    ]

    class Meta:
        indexes = [
            models.Index(fields=['-date',]),
        ]


class OfficialDocumentCollectionOfficialDocumentPage(ClusterableModel):
    page = ParentalKey(OfficialDocumentPage, related_name="official_document_collection")
    official_document_collection = models.ForeignKey('official_documents_collection.OfficialDocumentCollection',
                                                     verbose_name='Select an official document collection',
                                                     related_name='+', on_delete=models.CASCADE)
    panels = [
        PageChooserPanel('official_document_collection')
    ]

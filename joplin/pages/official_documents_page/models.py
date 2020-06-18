from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from base.forms import OfficialDocumentPageForm

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel

from base.models.constants import DEFAULT_MAX_LENGTH
from base.models.widgets import countMe, countMeTextArea, AUTHOR_LIMITS
from countable_field import widgets
from publish_preflight.requirements import FieldPublishRequirement, RelationPublishRequirement, \
    ConditionalPublishRequirement, DepartmentPublishRequirement

from pages.base_page.models import JanisBasePage
from pages.official_documents_list.models import OfficialDocumentList

"""
This is a page that displays a list of Official Documents (model: DocumentPageOfficialDocument).
This page can be assigned to multiple topics or departments.
The Documents will be displayed in date descending order (newest first by the "date" field).
Eventually the OfficialDocumentPageOfficialDocument should be replaced by a model using Wagtail Documents
"""


class OfficialDocumentPage(JanisBasePage):
    base_form_class = OfficialDocumentPageForm
    date = models.DateField(verbose_name="Document date", null=True)
    document_title = models.CharField(verbose_name="Document title", null=True, max_length=DEFAULT_MAX_LENGTH) #todo check null true
    authoring_office = models.CharField(verbose_name="Authoring office of document", null=True, max_length=DEFAULT_MAX_LENGTH) #todo check null true
    summary = models.TextField(verbose_name="Document summary")
    name = models.CharField(verbose_name="Name of Document", max_length=DEFAULT_MAX_LENGTH)
    document = models.ForeignKey(Document, null=True, blank=False, on_delete=models.SET_NULL, related_name='+',
                                 verbose_name="Document [en]")
    document_es = models.ForeignKey(Document, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
                                    verbose_name="Document [es]")

    publish_requirements = ()

    content_panels = [
        FieldPanel('date'),
        FieldPanel('document_title', widget=countMe),
        FieldPanel('authoring_office', widget=countMe),
        FieldPanel('summary', widget=widgets.CountableWidget(attrs={
            'data-count': 'characters',
            'data-max-count': AUTHOR_LIMITS['document_summary'],
            'data-count-direction': 'down'
        })),
        FieldPanel('name', widget=countMe),
        DocumentChooserPanel('document'),
        DocumentChooserPanel('document_es'),
        # InlinePanel('official_document_list', label="Official Document Lists this Document belongs to")
    ]

    # class Meta:
    #     indexes = [models.Index(fields=['-date'])]

    # publish_requirements = (
    #     FieldPublishRequirement("description", langs=["en"],
    #                             message="You need to write a description before publishing"),
    #     RelationPublishRequirement('documents'),
    #     ConditionalPublishRequirement(
    #         RelationPublishRequirement("topics"),
    #         "or",
    #         DepartmentPublishRequirement(),
    #         message="You must have at least 1 topic or 1 department selected.",
    #     )

#
# class OfficialDocumentPageDocumentList(ClusterableModel):
#     page = ParentalKey(OfficialDocumentPage, related_name="official_document_list")
#     official_document_list = models.ForeignKey('official_document_list.OfficialDocumentList',
#                                                verbose_name='Select an Official Document List',
#                                                related_name='+', on_delete=models.CASCADE)
#     panels = [
#         PageChooserPanel('official_document_list')
#     ]

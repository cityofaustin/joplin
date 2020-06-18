from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel
# from wagtail.core.models import Orderable
# # from wagtail.documents.models import Document
# from wagtail.documents.edit_handlers import DocumentChooserPanel

from pages.topic_page.models import JanisBasePageWithTopics
from base.forms import OfficialDocumentListForm
# from base.models.constants import DEFAULT_MAX_LENGTH
from base.models.widgets import countMe, countMeTextArea, AUTHOR_LIMITS
# from countable_field import widgets
from publish_preflight.requirements import FieldPublishRequirement, RelationPublishRequirement, \
     ConditionalPublishRequirement, DepartmentPublishRequirement


"""
This is a page that displays a list of Official Documents (model: DocumentPageOfficialDocument).
This page can be assigned to multiple topics or departments.
The Documents will be displayed in date descending order (newest first by the "date" field).
"""


class OfficialDocumentList(JanisBasePageWithTopics):
    janis_url_page_type = "official_document_list"
    base_form_class = OfficialDocumentListForm

    description = models.TextField(blank=True)

    publish_requirements = (
        # FieldPublishRequirement("description", langs=["en"],
        #                         message="You need to write a description before publishing"),
        # RelationPublishRequirement('documents'),
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
        # InlinePanel('documents_dos', label="Documents",
        #             heading="Entries will be listed by document date (newest first)."),
    ]

# class OfficialDocumentListDocument
#
# """
# An OfficialDocumentPageDocument is a Document belonging to a single OfficialDocumentPage.
# One OfficialDocumentPage can have many OfficialDocumentPageDocuments.
# """
#
#
# class OfficialDocumentPageDocument(Orderable):
#     page = ParentalKey(OfficialDocumentPage, related_name='documents_dos')
#     date = models.DateField(verbose_name="Document date", null=True)
#     title = models.CharField(verbose_name="Document title", max_length=DEFAULT_MAX_LENGTH)
#     authoring_office = models.CharField(verbose_name="Authoring office of document", max_length=DEFAULT_MAX_LENGTH)
#     summary = models.TextField(verbose_name="Document summary")
#     name = models.CharField(verbose_name="Name of Document", max_length=DEFAULT_MAX_LENGTH)
#     document = models.ForeignKey(Document, null=True, blank=False, on_delete=models.SET_NULL, related_name='+',
#                                  verbose_name="Document [en]")
#     document_es = models.ForeignKey(Document, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
#                                     verbose_name="Document [es]")
#
#     panels = [
#         FieldPanel('date'),
#         FieldPanel('title', widget=countMe),
#         FieldPanel('authoring_office', widget=countMe),
#         FieldPanel('summary', widget=widgets.CountableWidget(attrs={
#             'data-count': 'characters',
#             'data-max-count': AUTHOR_LIMITS['document_summary'],
#             'data-count-direction': 'down'
#         })),
#         FieldPanel('name', widget=countMe),
#         DocumentChooserPanel('document'),
#         DocumentChooserPanel('document_es')
#     ]
#
#     class Meta:
#         indexes = [models.Index(fields=['-date'])]


# class OfficialDocumentPageDocumentList(ClusterableModel):
#     page = ParentalKey(OfficialDocumentList, related_name="official_document_list")
#     official_document_list = models.ForeignKey('official_document_list.OfficialDocumentList',
#                                                verbose_name='Select an Official Document List',
#                                                related_name='+', on_delete=models.CASCADE)
#     panels = [
#         PageChooserPanel('official_document_list')
#     ]

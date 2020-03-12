from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.core.fields import StreamField
from wagtail.core.blocks import StructBlock, PageChooserBlock, TextBlock, ListBlock
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from base.forms import GuidePageForm

from pages.base_page.models import JanisBasePage
from pages.information_page.models import InformationPage
from pages.service_page.models import ServicePage
from base.models.contact import Contact
from base.models.translated_image import TranslatedImage

from base.models.widgets import countMe, countMeTextArea

from publish_preflight.requirements import FieldPublishRequirement, RelationPublishRequirement, StreamFieldPublishRequirement, ConditionalPublishRequirement, DepartmentPublishRequirement

from pages.topic_page.models import JanisBasePageWithTopics


def streamfield_has_pages(stream_value):
    """
    Confirms the stream_value has data, and
    the data contains both pages and an english section_heading
    :return: boolean
    """
    if stream_value:
        stream_data = stream_value.stream_data
        # check that we have any data in the streamfield
        if stream_data:
            struct_value = stream_data[0][1]
            if struct_value.get('pages') and struct_value.get('section_heading_en'):
                return True
    return False


class GuidePage(JanisBasePageWithTopics):
    """
    A guide page aggregates several pages together into a user-friendly view
    Since the number of related pages in a section could be arbitrary, it's
    implemented using Streamfields
    """
    janis_url_page_type = "guide"

    description = models.TextField(blank=True, verbose_name='Write a description of the guide')
    image = models.ForeignKey(TranslatedImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    sections = StreamField(
        [
            ('section', StructBlock(
                [
                    ('section_heading_en', TextBlock(label='Heading [en]')),
                    ('section_heading_es', TextBlock(label='Heading [es]', required=False)),
                    ('section_heading_ar', TextBlock(label='Heading [ar]', required=False)),
                    ('section_heading_vi', TextBlock(label='Heading [vi]', required=False)),
                    ('pages', ListBlock(
                        PageChooserBlock(label="Page", page_type=[InformationPage, ServicePage]),
                        help_text='Select existing pages in the order you want them \
                        to display within each heading.\
                        Pages should be added only once to any single guide.')
                     ),
                ],
                label="Section"
            )),
        ],
        verbose_name='Add a section header and pages to each section',
        blank=True
    )

    base_form_class = GuidePageForm

    publish_requirements = (
        FieldPublishRequirement("description", message="A description is required for publishing", langs=["en"]),
        RelationPublishRequirement("contacts", message="A contact is required for publishing."),
        StreamFieldPublishRequirement("sections", criteria=streamfield_has_pages),
        ConditionalPublishRequirement(
            RelationPublishRequirement("topics"),
            "or",
            DepartmentPublishRequirement(),
            message="You must have at least 1 topic or 1 department selected.",
        ),
    )

    content_panels = [
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('description', widget=countMeTextArea),
        InlinePanel('topics', label='Topics'),
        ImageChooserPanel('image'),
        StreamFieldPanel('sections'),
        InlinePanel('contacts', label='Contacts'),
    ]


class GuidePageContact(ClusterableModel):
    page = ParentalKey(GuidePage, related_name='contacts')
    contact = models.ForeignKey(Contact, related_name='+', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('contact'),
    ]

    def __str__(self):
        return self.contact.name

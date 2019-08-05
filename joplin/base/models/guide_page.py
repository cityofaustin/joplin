from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import RichTextBlock, StructBlock, PageChooserBlock, TextBlock, ListBlock
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel

from base.forms import GuidePageForm

from .janis_page import JanisPage
from .contact import Contact
from .translated_image import TranslatedImage

from .constants import WYSIWYG_GENERAL

class GuidePage(JanisPage):
    janis_url_page_type = "guide"

    description = models.TextField(blank=True, verbose_name='Write a description of the guide')
    image = models.ForeignKey(TranslatedImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

# label="Select existing pages in the order you want them to display within each heading. Pages should be added only once to any single guide."
    sections = StreamField(
        [
            ('section', StructBlock(
                [
                    ('section_heading', TextBlock('Heading')),
                    ('pages', ListBlock(PageChooserBlock(label="Page"))),
                ],
                label="Section"
            )),
        ],
        verbose_name='Add a section header and pages to each section',
        # this gets called in the help panel
        # help_text='A step may have a basic text step or an options accordion which reveals two or more options',
        blank=True
    )





    base_form_class = GuidePageForm

    content_panels = [
        FieldPanel('title_en'),
        FieldPanel('title_es'),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('description'),
        InlinePanel('topics', label='Topics'),
        InlinePanel('related_departments', label='Related Departments'),
        # InlinePanel('sections', label='Add a section header and pages to each section'),
        ImageChooserPanel('image'),
        StreamFieldPanel('sections'),
        InlinePanel('contacts', label='Contacts'),
    ]

# class GuidePageSection(Orderable):
#     guide_page = ParentalKey(GuidePage, related_name='sections')
#     heading = models.TextField(blank=True, verbose_name='Heading')
    

#     panels = [
#       FieldPanel('heading'),
#       InlinePanel('section_pages', label='Select existing pages in the order you want them to display within each heading. Pages should be added only once to any single guide.'),
#     ]

#     def __str__(self):
#         return self.heading.text


# class GuidePageSectionPage(Orderable):
#     section = ParentalKey(GuidePageSection, related_name='section_pages')
#     page = models.ForeignKey('base.JanisBasePage',  verbose_name='Select a Page', related_name='+', on_delete=models.CASCADE)

#     panels = [
#         PageChooserPanel("page"),
#     ]

#     def __str__(self):
#         return self.page.text

class GuidePageTopic(ClusterableModel):
    page = ParentalKey(GuidePage, related_name='topics')
    topic = models.ForeignKey('base.TopicPage',  verbose_name='Select a Topic', related_name='+', on_delete=models.CASCADE)
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

class GuidePageRelatedDepartments(ClusterableModel):
    page = ParentalKey(GuidePage, related_name='related_departments', default=None)
    related_department = models.ForeignKey(
        "base.departmentPage",
        on_delete=models.PROTECT,
    )

    panels = [
        # Use a SnippetChooserPanel because blog.BlogAuthor is registered as a snippet
        PageChooserPanel("related_department"),
    ]

class GuidePageContact(ClusterableModel):
    page = ParentalKey(GuidePage, related_name='contacts')
    contact = models.ForeignKey(Contact, related_name='+', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('contact'),
    ]

    def __str__(self):
        return self.contact.name



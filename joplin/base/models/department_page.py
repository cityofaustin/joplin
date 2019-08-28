from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Orderable
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from base.forms import DepartmentPageForm

from .janis_page import JanisBasePage
from .information_page import InformationPage
from .service_page import ServicePage
from .guide_page import GuidePage
from .translated_image import TranslatedImage
from .contact import Contact

from .constants import DEFAULT_MAX_LENGTH, WYSIWYG_GENERAL


class DepartmentPage(JanisBasePage):
    janis_url_page_type = "department"

    def __str__(self):
        return self.title_en

    what_we_do = RichTextField(
        features=WYSIWYG_GENERAL,
        verbose_name='What we do',
        blank=True
    )

    image = models.ForeignKey(TranslatedImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    mission = models.TextField(
        verbose_name='Mission',
    )

    job_listings = models.URLField(
        verbose_name='Job listings url',
        help_text='Link to a page with job listings.',
        blank=True
    )

    # top_services = StreamField(
    #     [
    #         ('pages', ListBlock(PageChooserBlock(label="Page", page_type=[InformationPage, ServicePage, GuidePage]),
    #                             help_text='Add links to 1-4 top service pages or guides (4 maximum allowed).')),
    #     ],
    #     verbose_name='Links to top services',
    #     blank=True
    # )

    base_form_class = DepartmentPageForm

    content_panels = [
        FieldPanel('title_en'),
        FieldPanel('title_es'),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('what_we_do'),
        ImageChooserPanel('image'),
        FieldPanel('mission'),
        InlinePanel('contacts', label='Contacts'),
        InlinePanel('department_directors', label="Department Directors"),
        FieldPanel('job_listings'),
        InlinePanel('top_services', heading='HEAD', label='LABEL', help_text='HELP', min_num=None, max_num=4)
    ]


class DepartmentPageDirector(Orderable):
    page = ParentalKey(DepartmentPage, related_name='department_directors')
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    title = models.CharField(max_length=DEFAULT_MAX_LENGTH, default='Director')
    photo = models.ForeignKey(TranslatedImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    about = models.TextField(blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('title'),
        ImageChooserPanel('photo'),
        FieldPanel('about'),
    ]


class DepartmentPageContact(ClusterableModel):
    page = ParentalKey(DepartmentPage, related_name='contacts')
    contact = models.ForeignKey(Contact, related_name='+', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('contact'),
    ]

    def __str__(self):
        return self.contact.name


class DepartmentPageTopServices(ClusterableModel):
    department = ParentalKey(DepartmentPage, related_name='top_services')
    page = models.ForeignKey('wagtailcore.Page',  verbose_name='Select a page', related_name='+', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('page', page_type=[InformationPage, ServicePage, GuidePage]),
    ]

    def __str__(self):
        return self.page.text

from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Orderable
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from base.forms import DepartmentPageForm

from pages.base_page.models import JanisBasePage
from pages.information_page.models import InformationPage
from pages.service_page.models import ServicePage
from pages.guide_page.models import GuidePage
from pages.official_documents_page.models import OfficialDocumentPage
from base.models.translated_image import TranslatedImage
from base.models.contact import Contact

from base.models.constants import DEFAULT_MAX_LENGTH, WYSIWYG_GENERAL
from base.models.widgets import countMe, AUTHOR_LIMITS
from countable_field import widgets
from publish_preflight.requirements import FieldPublishRequirement


class DepartmentPage(JanisBasePage):
    """
    A base that contains information about a department for public consumption
    Note: there also may be other department models used for internally managing
    content, user permissions, etc
    """

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
        blank=True
    )

    job_listings = models.URLField(
        verbose_name='Job listings url',
        help_text='Link to a page with job listings.',
        blank=True
    )

    base_form_class = DepartmentPageForm

    publish_requirements = (
        FieldPublishRequirement("what_we_do", langs=["en"]),
    )

    content_panels = [
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('what_we_do'),
        ImageChooserPanel('image'),
        FieldPanel('mission', widget=widgets.CountableWidget(attrs={
            'data-count': 'characters',
            'data-max-count': AUTHOR_LIMITS['mission'],
            'data-count-direction': 'down'
        })),
        InlinePanel('contacts', label='Contacts'),
        InlinePanel('department_directors', label="Department Directors"),
        FieldPanel('job_listings'),
        InlinePanel('top_pages', heading='Links to top services', label='top link',
                    help_text='Add links to 1-4 top service pages or guides (4 maximum allowed).',
                    min_num=None, max_num=4),
        InlinePanel('related_pages', heading='Links to related pages', label='related page',
                    help_text='Add links to 1-4 related information pages or guides (4 maximum allowed).',
                    min_num=None, max_num=4)
    ]

    def janis_urls(self):
        """
        Department pages should have at most one url
        """

        # check the one to one relationship of pages to department groups
        # it's the only time we should have a url for a department page
        if hasattr(self, 'department'):
            return ['{base_url}{page_slug}/'.format(base_url=self.janis_url_base('publish_janis_branch'),
                                                    page_slug=self.slug)]

        return []


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
        FieldPanel('about', widget=widgets.CountableWidget(attrs={
            'data-count': 'characters',
            'data-max-count': AUTHOR_LIMITS['about_director'],
            'data-count-direction': 'down'
        }))
    ]


class DepartmentPageContact(ClusterableModel):
    page = ParentalKey(DepartmentPage, related_name='contacts')
    contact = models.ForeignKey(Contact, related_name='+', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('contact'),
    ]

    def __str__(self):
        return self.contact.name


class DepartmentPageTopPage(Orderable):
    department = ParentalKey(DepartmentPage, related_name='top_pages')
    page = models.ForeignKey('wagtailcore.Page', verbose_name='Select a page', related_name='+', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('page', page_type=[InformationPage, ServicePage, GuidePage, OfficialDocumentPage]),
    ]

    def __str__(self):
        return self.page.text


class DepartmentPageRelatedPage(Orderable):
    department = ParentalKey(DepartmentPage, related_name='related_pages')
    page = models.ForeignKey('wagtailcore.Page', verbose_name='Select a page', related_name='+', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('page', page_type=[InformationPage, ServicePage, GuidePage, OfficialDocumentPage]),
    ]

    def __str__(self):
        return self.page.text
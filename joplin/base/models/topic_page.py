from django.db import models

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Orderable

from .information_page import InformationPage
from .service_page import ServicePage
from .guide_page import GuidePage
from .official_documents_page import OfficialDocumentPage

from base.forms import TopicPageForm

from .janis_page import JanisBasePage
from .translated_image import TranslatedImage
from .widgets import countMe, countMeTextArea


class TopicPage(JanisBasePage):
    janis_url_page_type = "topic"

    description = models.TextField(blank=True)

    image = models.ForeignKey(TranslatedImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    base_form_class = TopicPageForm

    content_panels = [
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('description', widget=countMeTextArea),
        ImageChooserPanel('image'),
        InlinePanel('topiccollections', label='Topic Collections this page belongs to'),
        InlinePanel('top_pages', heading='Links to top pages', label='top link',
                    help_text='Add links to 1-4 top pages or guides (4 maximum allowed).',
                    min_num=None, max_num=4),
    ]


class TopicPageTopPage(Orderable):
    topic = ParentalKey(TopicPage, related_name='top_pages')
    page = models.ForeignKey('wagtailcore.Page',  verbose_name='Select a page', related_name='+', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('page', page_type=[InformationPage, ServicePage, GuidePage, OfficialDocumentPage]),
    ]

    # this errors because it says page has no attribute text, can we fall back on the original method?
    # def __str__(self):
    #     return self.page.text


class TopicPageTopicCollection(ClusterableModel):
    page = ParentalKey(TopicPage, related_name='topiccollections')
    topiccollection = models.ForeignKey('base.TopicCollectionPage', verbose_name='Select a Topic Collection', related_name='+', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('topiccollection'),
    ]

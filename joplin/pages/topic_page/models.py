from django.db import models

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Orderable

from pages.information_page.models import InformationPage
from pages.service_page.models import ServicePage
from pages.guide_page.models import GuidePage
from pages.official_documents_page.models import OfficialDocumentPage

from base.forms import TopicPageForm

from pages.base_page.models import JanisBasePage
from pages.topic_collection_page.models import JanisBasePageWithTopicCollections
from base.models.translated_image import TranslatedImage
from base.models.widgets import countMe, countMeTextArea
from publish_preflight.requirements import RelationPublishRequirement


class TopicPage(JanisBasePageWithTopicCollections):
    janis_url_page_type = "topic"

    description = models.TextField(blank=True)

    image = models.ForeignKey(TranslatedImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    base_form_class = TopicPageForm

    publish_requirements = (
        RelationPublishRequirement('top_pages'),
        RelationPublishRequirement('topic_collections'),
    )

    content_panels = [
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('description', widget=countMeTextArea),
        ImageChooserPanel('image'),
        InlinePanel('topic_collections', label='Topic Collections this page belongs to'),
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

    def __str__(self):
        return self.page.title


class JanisBasePageWithTopics(JanisBasePage):
    pass


class JanisBasePageTopic(ClusterableModel):
    page = ParentalKey(JanisBasePageWithTopics, related_name='topics')
    topic = models.ForeignKey('topic_page.TopicPage', verbose_name='Select a Topic', related_name='+',
                              on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('topic'),
    ]

    def __str__(self):
        return self.topic.text

from django.db import models

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Orderable

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
        # RelationPublishRequirement('top_pages'),
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
    page = models.ForeignKey('wagtailcore.Page', verbose_name='Select a page', related_name='+',
                             on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('page', page_type=['information_page.InformationPage', 'service_page.ServicePage',
                                            'guide_page.GuidePage', 'official_documents_page.OfficialDocumentPage']),
    ]

    def __str__(self):
        return self.page.title


class JanisBasePageWithTopics(JanisBasePage):
    def janis_urls(self):
        # get the base urls (global/department)
        urls = super().janis_urls()

        # if we're global, skip topics
        # todo: verify this logic
        if self.coa_global:
            return urls

        for base_page_topic in self.topics.all():
            for topic_page_url in base_page_topic.topic.janis_urls():
                tu = topic_page_url
                urls.extend([{
                    'url': "{topic_page_url}{page_slug}".format(topic_page_url=topic_page_url['url'], page_slug=self.slug),
                    'parent': base_page_topic.topic,
                    'grandparent': topic_page_url['parent']}])
                print(urls)
        return urls

    def departments(self):
        departments = super().departments()

        return departments


class JanisBasePageTopic(ClusterableModel):
    page = ParentalKey(JanisBasePageWithTopics, related_name='topics')
    topic = models.ForeignKey('topic_page.TopicPage', verbose_name='Select a Topic', related_name='+',
                              on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('topic'),
    ]

    def __str__(self):
        return self.topic.text

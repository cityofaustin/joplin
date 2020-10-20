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
        FieldPanel('slug_en'),
        FieldPanel('slug_es'),
        FieldPanel('slug_ar'),
        FieldPanel('slug_vi'),
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
                                            'guide_page.GuidePage', 'official_documents_collection.OfficialDocumentCollection']),
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
            urls.extend(['{topic_page_url}{page_slug}/'.format(topic_page_url=topic_page_url, page_slug=self.slug_en) for
                         topic_page_url in base_page_topic.topic.janis_urls()])

        return urls

    def janis_instances(self):
        # get the base urls (global/department)
        instances = super().janis_instances()

        # if we're global, skip topics
        # todo: verify this logic -- check if we need this
        if self.coa_global:
            return instances

        for base_page_topic in self.topics.all():
            for topic_page_url in base_page_topic.topic.janis_instances():
                instances.extend([{
                    'url': "{topic_page_url}{page_slug}".format(topic_page_url=topic_page_url['url'], page_slug=self.slug_en),
                    'parent': base_page_topic.topic,
                    'grandparent': topic_page_url['parent']}])
        return instances

    def departments(self):
        departments = super().departments()

        return departments

    @property
    def search_output(self):
        output = {}
        output.update(super().search_output)
        output["topics"] = [{
            "title": t.topic.title,
            "url": t.topic.janis_urls() and t.topic.janis_urls()[0],
        } for t in self.specific.topics.all()]
        return output


class JanisBasePageTopic(ClusterableModel):
    page = ParentalKey(JanisBasePageWithTopics, related_name='topics')
    topic = models.ForeignKey('topic_page.TopicPage', verbose_name='Select a Topic', related_name='+',
                              on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('topic'),
    ]

    def __str__(self):
        return self.topic.title

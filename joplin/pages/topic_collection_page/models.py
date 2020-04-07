from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from base.forms import TopicCollectionPageForm

from pages.base_page.models import JanisBasePage
from base.models.translated_image import TranslatedImage
from base.models.widgets import countMe, countMeTextArea
from publish_preflight.requirements import FieldPublishRequirement


class TopicCollectionPage(JanisBasePage):
    janis_url_page_type = "topiccollection"

    description = models.TextField(blank=True)

    theme = models.ForeignKey(
        'base.Theme',
        on_delete=models.PROTECT,
        related_name='topic_collection_pages',
        null=True, blank=True,
    )

    image = models.ForeignKey(TranslatedImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    base_form_class = TopicCollectionPageForm

    publish_requirements = (
        FieldPublishRequirement('theme'),
    )

    content_panels = [
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('description', widget=countMeTextArea),
        FieldPanel('theme'),
        ImageChooserPanel('image'),
    ]

    def janis_urls(self):
        # should publish at /theme_slug/topic_collection_slug/
        if self.theme.slug:
            return [f'{self.theme.slug}/{self.slug}/']

        return []

    def janis_instances(self):
        if self.theme.slug:
            return [
                {'url': f'{self.theme.slug}/{self.slug}/'}
                # do I need to include the grandparent here? tc dont have CN but extending....?
            ]

        return []


class JanisBasePageWithTopicCollections(JanisBasePage):
    def janis_urls(self):
        # Add the urls for each topic collection, these pages only
        # should publish at /theme_slug/topic_collection_slug/topic_page_slug
        urls = []

        for base_page_topic_collection in self.topic_collections.all():
            for topic_collection_url in base_page_topic_collection.topic_collection.janis_urls():
                urls.append({
                    'url': f'/{topic_collection_url}{self.slug}/',
                    'parent': base_page_topic_collection.topic_collection
                })

        return urls


class JanisBasePageTopicCollection(ClusterableModel):
    page = ParentalKey(JanisBasePageWithTopicCollections, related_name='topic_collections')
    topic_collection = models.ForeignKey('topic_collection_page.TopicCollectionPage',
                                         verbose_name='Select a Topic Collection', related_name='+',
                                         on_delete=models.CASCADE)
    panels = [
        PageChooserPanel('topic_collection'),
    ]

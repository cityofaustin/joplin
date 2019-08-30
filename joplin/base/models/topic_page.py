from django.db import models

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.core.fields import StreamField
from wagtail.core.blocks import CharBlock, StructBlock, URLBlock
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from base.forms import TopicPageForm

from .janis_page import JanisBasePage
from .translated_image import TranslatedImage


class TopicPage(JanisBasePage):
    janis_url_page_type = "topic"

    description = models.TextField(blank=True)

    image = models.ForeignKey(TranslatedImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    external_services = StreamField(
        [
            ('link_en', StructBlock([
                ('url', URLBlock()),
                ('title', CharBlock()),
            ], icon='link', label='Link [EN]')),
            ('link_es', StructBlock([
                ('url', URLBlock()),
                ('title', CharBlock()),
            ], icon='link', label='Link [ES]')),
            ('link_ar', StructBlock([
                ('url', URLBlock()),
                ('title', CharBlock()),
            ], icon='link', label='Link [AR]')),
            ('link_vi', StructBlock([
                ('url', URLBlock()),
                ('title', CharBlock()),
            ], icon='link', label='Link [VI]')),
        ],
        verbose_name='External links to services',
        blank=True
    )

    base_form_class = TopicPageForm

    content_panels = [
        FieldPanel('title_en'),
        FieldPanel('title_es'),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('description'),
        ImageChooserPanel('image'),
        StreamFieldPanel('external_services'),
        InlinePanel('topiccollections', label='Topic Collections this page belongs to'),
    ]


class TopicPageTopicCollection(ClusterableModel):
    page = ParentalKey(TopicPage, related_name='topiccollections')
    topiccollection = models.ForeignKey('base.TopicCollectionPage', verbose_name='Select a Topic Collection', related_name='+', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('topiccollection'),
    ]

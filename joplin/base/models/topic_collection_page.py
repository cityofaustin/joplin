from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel

from base.forms import TopicCollectionPageForm

from .janis_page import JanisBasePage
from .translated_image import TranslatedImage
from .widgets import countMe, countMeTextArea
from publish_preflight.requirements import FieldPublishRequirement


class TopicCollectionPage(JanisBasePage):
    janis_url_page_type = "topiccollection"

    description = models.TextField(blank=True)

    theme = models.ForeignKey(
        'base.Theme',
        on_delete=models.PROTECT,
        related_name='topicCollectionPages',
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
        InlinePanel('topiccollections', label='Topic Collections this page belongs to'),
    ]

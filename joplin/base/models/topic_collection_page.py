from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel

from base.forms import TopicCollectionPageForm

from .janis_page import JanisBasePage
from .translated_image import TranslatedImage


class TopicCollectionPage(JanisBasePage):
    janis_url_page_type = "topiccollection"

    theme = models.ForeignKey(
        'base.Theme',
        on_delete=models.PROTECT,
        related_name='topicCollectionPages',
        null=True, blank=True,
    )

    image = models.ForeignKey(TranslatedImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    base_form_class = TopicCollectionPageForm

    content_panels = JanisBasePage.content_panels + [
        FieldPanel('theme'),
        ImageChooserPanel('image'),
        InlinePanel('topiccollections', label='Topic Collections this page belongs to'),
    ]

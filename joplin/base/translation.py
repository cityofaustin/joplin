from modeltranslation.translator import register, TranslationOptions
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.models import Image

from .models import Topic, ServicePage, TranslatedImage


@register(Image)
class ImageTranslationOptions(TranslationOptions):
    pass


@register(TranslatedImage)
class TranslatedImageTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


@register(Topic)
class TopicTranslationOptions(TranslationOptions):
    fields = (
        'text',
        'description',
    )


@register(Page)
class PageTranslationOptions(TranslationOptions):
    pass


@register(ServicePage)
class ServicePageTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'steps',
        'additional_content',
    )

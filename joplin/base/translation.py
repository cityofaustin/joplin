from modeltranslation.translator import register, TranslationOptions
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.models import Image

from .models import Topic, ServicePage, TranslatedImage, Department, Map


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


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'mission',
    )


@register(Map)
class MapTranslationOptions(TranslationOptions):
    fields = (
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

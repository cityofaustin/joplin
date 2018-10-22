from modeltranslation.translator import register, TranslationOptions
from wagtail.core.models import Page
from wagtail.images.models import Image

from .models import ThreeOneOne, Topic, Theme, ServicePage, ProcessPage, ProcessPageStep, TranslatedImage, Department, Map


@register(Image)
class ImageTranslationOptions(TranslationOptions):
    pass


@register(TranslatedImage)
class TranslatedImageTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


@register(ThreeOneOne)
class ThreeOneOneTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


@register(Topic)
class TopicTranslationOptions(TranslationOptions):
    fields = (
        'text',
        'description',
        'call_to_action',
    )


@register(Theme)
class ThemeTranslationOptions(TranslationOptions):
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
        'additional_content',
    )

@register(ProcessPage)
class ProcessPageTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'description'
    )

@register(ProcessPageStep)
class ProcessPageStepTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'short_title',
        'link_title',
        'description',
        'overview_steps',
        'detailed_content',
        'quote'
    )

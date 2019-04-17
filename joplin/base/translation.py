from wagtail_modeltranslation.translation import register, TranslationOptions
from wagtail.core.models import Page
from wagtail.images.models import Image

from .models import ThreeOneOne, TopicPage, Theme, ServicePage, ProcessPage, ProcessPageStep, DepartmentPage, DepartmentPageDirector, InformationPage, TranslatedImage, Department, Map, HomePage


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
    

@register(TopicPage)
class TopicPageTranslationOptions(TranslationOptions):
    fields = (
        'description',
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


@register(HomePage)
class HomePageTranslationOptions(TranslationOptions):
    pass

@register(ServicePage)
class ServicePageTranslationOptions(TranslationOptions):
    fields = (
        'additional_content',
    )

@register(ProcessPage)
class ProcessPageTranslationOptions(TranslationOptions):
    fields = (
        'description',
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
        'quote',
    )

@register(DepartmentPage)
class DepartmentPageTranslationOptions(TranslationOptions):
    fields = (
        'what_we_do',
        'mission',
    )

@register(DepartmentPageDirector)
class DepartmentPageDirectorTranslationOptions(TranslationOptions):
    fields = (
        'about',
        'title'
    )

@register(InformationPage)
class InformationPageTranslationOptions(TranslationOptions):
    fields = (
        'description',
        'options',
        'additional_content',
    )
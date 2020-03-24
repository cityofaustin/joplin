from wagtail_modeltranslation.translation import register, TranslationOptions
from wagtail.core.models import Page
from wagtail.images.models import Image


from .models import ThreeOneOne, TopicPage, TopicCollectionPage, Theme, ServicePage, ProcessPage, ProcessPageStep, \
    DepartmentPage, DepartmentPageDirector, InformationPage, OfficialDocumentPage,\
    OfficialDocumentPageOfficialDocument, TranslatedImage, Map, HomePage, GuidePage, FormContainer
from locations.models import LocationPage, LocationPageRelatedServices
from events.models import EventPage, EventPageFee


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


@register(TopicCollectionPage)
class TopicCollectionPageTranslationOptions(TranslationOptions):
    fields = (
        'description',
    )


@register(Theme)
class ThemeTranslationOptions(TranslationOptions):
    fields = (
        'text',
        'description',
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
        'steps',
        'short_description',
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


@register(OfficialDocumentPage)
class OfficialDocumentPageTranslationOptions(TranslationOptions):
    fields = (
        'description',
    )


@register(OfficialDocumentPageOfficialDocument)
class OfficialDocumentPageOfficialDocumentTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'summary',
        'name',
        'authoring_office'
    )


@register(GuidePage)
class GuidePageTranslationOptions(TranslationOptions):
    fields = (
        'description',
    )


@register(FormContainer)
class FormContainerTranslationOptions(TranslationOptions):
    fields = (
        'description',
        'form_url',
    )


@register(LocationPage)
class LocationPageOptions(TranslationOptions):
    fields = (
        'hours_exceptions',
    )


@register(EventPage)
class EventPageTranslationOptions(TranslationOptions):
    fields = (
        'description',
    )


@register(EventPageFee)
class EventPageFeeTranslationOptions(TranslationOptions):
    fields = (
        'fee_label',
    )

@register(LocationPageRelatedServices)
class LocationPageRelatedServicesTranslationOptions(TranslationOptions):
    fields = (
        'hours_exceptions',
    )


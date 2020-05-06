from wagtail_modeltranslation.translation import register, TranslationOptions
from wagtail.core.models import Page
from wagtail.images.models import Image

from base.models import TranslatedImage
from snippets.theme.models import Theme
from pages.base_page.models import JanisBasePage
from pages.topic_collection_page.models import TopicCollectionPage
from pages.topic_page.models import TopicPage, TopicPageTopPage
from pages.service_page.models import ServicePage
from pages.information_page.models import InformationPage
from pages.department_page.models import DepartmentPage, DepartmentPageDirector, DepartmentPageTopPage, DepartmentPageRelatedPage
from pages.official_documents_page.models import OfficialDocumentPage, OfficialDocumentPageDocument
from pages.guide_page.models import GuidePage
from pages.form_container.models import FormContainer
from pages.home_page.models import HomePage
from pages.location_page.models import LocationPage, LocationPageRelatedServices
from pages.event_page.models import EventPage, EventPageFee
from pages.news_page.models import NewsPage


@register(Image)
class ImageTranslationOptions(TranslationOptions):
    pass


@register(TranslatedImage)
class TranslatedImageTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


@register(JanisBasePage)
class JanisBasePageTranslationOptions(TranslationOptions):
    pass


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
        'additional_content',
    )


@register(OfficialDocumentPage)
class OfficialDocumentPageTranslationOptions(TranslationOptions):
    fields = (
        'description',
    )


@register(OfficialDocumentPageDocument)
class OfficialDocumentPageDocumentTranslationOptions(TranslationOptions):
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

@register(NewsPage)
class MediaReleasePageTranslationOptions(TranslationOptions):
    fields = (
        'body',
    )

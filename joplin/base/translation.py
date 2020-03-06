from wagtail_modeltranslation.translation import register, TranslationOptions
from wagtail.core.models import Page
from wagtail.images.models import Image

from base.models import TranslatedImage, Theme, Contact, Location, PhoneNumber, ContactDayAndDuration, ThreeOneOne, Map, HomePage

from pages.topic_collection_page.models import TopicCollectionPage
from pages.topic_page.models import TopicPage, TopicPageTopicCollection, TopicPageTopPage
from pages.service_page.models import ServicePage, ServicePageTopic, ServicePageContact
from pages.information_page.models import InformationPage, InformationPageTopic, InformationPageContact
from pages.department_page.models import DepartmentPage, DepartmentPageDirector, DepartmentPageContact, DepartmentPageTopPage, DepartmentPageRelatedPage
from pages.official_documents_page.models import OfficialDocumentPage, OfficialDocumentPageOfficialDocument, OfficialDocumentPageTopic
from pages.guide_page.models import GuidePage, GuidePageTopic, GuidePageContact
from pages.form_container.models import FormContainer, FormContainerTopic


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


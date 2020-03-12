import factory
import wagtail_factories
from django.utils.text import slugify
from wagtail.core.models import Collection, Page
from pages.official_documents_page.models import OfficialDocumentPage, OfficialDocumentPageTopic
from pages.factory import PageFactory
from pages.topic_page_factories import TopicPageFactory

from pages.base_page.factories import JanisBasePageWithTopicsFactory


class OfficialDocumentPageFactory(JanisBasePageWithTopicsFactory):
    class Meta:
        model = OfficialDocumentPage


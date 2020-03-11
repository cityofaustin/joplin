import factory
import wagtail_factories
from django.utils.text import slugify
from wagtail.core.models import Collection, Page
from pages.official_documents_page.models import OfficialDocumentPage
from pages.factory import PageFactory


class OfficialDocumentPageFactory(PageFactory):
    class Meta:
        model = OfficialDocumentPage

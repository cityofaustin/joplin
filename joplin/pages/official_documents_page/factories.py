import factory
import wagtail_factories
from django.utils.text import slugify
from wagtail.core.models import Collection, Page
from pages.official_documents_page.models import OfficialDocumentPage, OfficialDocumentPageTopic
from pages.factory import PageFactory
from pages.topic_page_factories import TopicPageFactory



class OfficialDocumentPageTopicFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('official_documents_page.factories.GuidePageFactory')
    topic = TopicPageFactory(parent=home_page)

    class Meta:
        model = OfficialDocumentPageTopic






class OfficialDocumentPageFactory(PageFactory):
    class Meta:
        model = OfficialDocumentPage

    @factory.post_generation
    def create_related_objects(self, create, extracted, **kwargs):
        if create:
            OfficialDocumentPageTopicFactory.create_batch(2, page=self)

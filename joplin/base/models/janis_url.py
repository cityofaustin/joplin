from django.db import models
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
# from wagtail.snippets.models import register_snippet

from .topic_collection_page import TopicCollectionPage
from .topic_page import TopicPage
from .department_page import DepartmentPage


class DepartmentPageJanisUrl(ClusterableModel):
    page = ParentalKey(DepartmentPage, related_name='janis_urls')
    janis_url = models.ForeignKey('base.JanisUrl', verbose_name='URL', related_name='+', on_delete=models.CASCADE)


class TopicCollectionPageJanisUrl(ClusterableModel):
    page = ParentalKey(TopicCollectionPage, related_name='janis_urls')
    janis_url = models.ForeignKey('base.JanisUrl', verbose_name='URL', related_name='+', on_delete=models.CASCADE)


class TopicPageJanisUrl(ClusterableModel):
    page = ParentalKey(TopicPage, related_name='janis_urls')
    janis_url = models.ForeignKey('base.JanisUrl', verbose_name='URL', related_name='+', on_delete=models.CASCADE)


# @register_snippet
class JanisUrl(models.Model):
    url = models.CharField(max_length=9001)
    language = models.CharField(max_length=9)

    # Themes don't have dedicated pages
    theme = models.ForeignKey('base.Theme', on_delete=models.PROTECT,null=True, blank=True)

    topic_collection_page = models.ForeignKey('base.TopicCollectionPage', on_delete=models.CASCADE, null=True, blank=True)
    topic_page = models.ForeignKey('base.TopicPage', on_delete=models.CASCADE, null=True, blank=True)
    department_page = models.ForeignKey("base.departmentPage",on_delete=models.PROTECT, null=True, blank=True)

    # Location page urls are always:
    # /location/location_slug/
    location_page = models.ForeignKey("locations.LocationPage",on_delete=models.PROTECT, null=True, blank=True)

    # The rest of the pages follow these url structures:
    # /theme_slug/topic_collection_slug/topic_slug/page_slug/
    # /department_slug/page_slug/
    # /page_slug/
    information_page = models.ForeignKey("base.InformationPage", on_delete=models.PROTECT, null=True, blank=True)
    service_page = models.ForeignKey("base.ServicePage", on_delete=models.PROTECT, null=True, blank=True)
    guide_page = models.ForeignKey("base.GuidePage", on_delete=models.PROTECT, null=True, blank=True)
    official_documents_page = models.ForeignKey("base.OfficialDocumentPage", on_delete=models.PROTECT, null=True, blank=True)
    form_container = models.ForeignKey("base.FormContainer", on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.url

    @staticmethod
    def get_translated_slug(language, page):
        # todo: flesh this out
        if language == 'es':
            if page.slug_es:
                return page.slug_es

        return page.slug_en

    @classmethod
    def create(cls, page_type, language, theme=None, topic_collection_page=None, topic_page=None, department_page=None):
        # Topic collection pages urls are always:
        # /theme_slug/topic_collection_slug/
        if page_type == 'TopicCollectionPage':
            new_janis_url = cls(theme=theme,
                                topic_collection_page=topic_collection_page,
                                url=f'''/{language}/{theme.slug}/{
                                    JanisUrl.get_translated_slug(language, topic_collection_page)
                                }/''')

        # Topic page urls are always:
        # /theme_slug/topic_collection_slug/topic_slug/
        if page_type == 'TopicPage':
            new_janis_url = cls(theme=theme,
                                topic_collection_page=topic_collection_page,
                                topic_page=topic_page,
                                url=f'''/{language}/{theme.slug}/{
                                    JanisUrl.get_translated_slug(language, topic_collection_page)
                                }/{
                                    JanisUrl.get_translated_slug(language, topic_page)
                                }/''')

        # Department page urls are always:
        # /department_slug/
        if page_type == 'DepartmentPage':
            new_janis_url = cls(department_page=department_page,
                                url=f'/{language}/{JanisUrl.get_translated_slug(language, department_page)}/')

        return new_janis_url

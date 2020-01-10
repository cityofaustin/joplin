from django.db import models
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
# from wagtail.snippets.models import register_snippet

# @register_snippet
class JanisUrl(ClusterableModel):
    url = models.CharField()

    page = ParentalKey(JanisPage, related_name='janis_urls', default=None)
    
    theme = models.ForeignKey('base.Theme',on_delete=models.PROTECT,null=True, blank=True)
    topic_collection = models.ForeignKey('base.TopicCollectionPage', on_delete=models.CASCADE,null=True, blank=True)
    topic = models.ForeignKey('base.TopicPage', on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey("base.departmentPage",on_delete=models.PROTECT, null=True, blank=True)
    
    language = models.CharField()

    def __str__(self):
        return self.url

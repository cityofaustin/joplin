from django.db import models
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
# from wagtail.snippets.models import register_snippet

class TopicPageJanisUrl(ClusterableModel):
    page = ParentalKey(TopicPage, related_name='janis_urls')
    janis_url = models.ForeignKey('base.JanisUrl', verbose_name='URL', related_name='+', on_delete=models.CASCADE)

    # panels = [
    #     PageChooserPanel('topiccollection'),
    # ]

# @register_snippet
class JanisUrl(models.Model):
    url = models.CharField(max_length=9001)

    # page = ParentalKey(JanisPage, related_name='janis_urls', default=None)
    
    page = models.ForeignKey('base.JanisBasePage',on_delete=models.PROTECT,null=True, blank=True)
    theme = models.ForeignKey('base.Theme',on_delete=models.PROTECT,null=True, blank=True)
    topic_collection = models.ForeignKey('base.TopicCollectionPage', on_delete=models.CASCADE,null=True, blank=True)
    topic = models.ForeignKey('base.TopicPage', on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey("base.departmentPage",on_delete=models.PROTECT, null=True, blank=True)
    
    language = models.CharField(max_length=9)

    def __str__(self):
        return self.url

from django.db import models
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.snippets.models import register_snippet
from .janis_page import JanisBasePage
from wagtail.admin.edit_handlers import InlinePanel
import uuid

class JanisUrlPage(ClusterableModel):
    # to allow for multiple inheritance to work, we need to avoid clashes
    # this makes it so we don't have 2 fields named id
    # https://stackoverflow.com/questions/35109940/custom-id-field-in-django-model
    url_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    notes_content_panel = [
        InlinePanel('janis_urls', label="Janis URLs")
    ]

    # class Meta:
    #     abstract = True

@register_snippet
class JanisUrl(ClusterableModel):
    url = models.CharField(max_length=9001)

    page = ParentalKey(JanisUrlPage, related_name='janis_urls', default=None)
    
    theme = models.ForeignKey('base.Theme',on_delete=models.PROTECT,null=True, blank=True)
    topic_collection = models.ForeignKey('base.TopicCollectionPage', on_delete=models.CASCADE,null=True, blank=True)
    topic = models.ForeignKey('base.TopicPage', on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey("base.departmentPage",on_delete=models.PROTECT, null=True, blank=True)
    
    language = models.CharField(max_length=9)

    def __str__(self):
        return self.url

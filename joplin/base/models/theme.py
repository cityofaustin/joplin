from django.db import models

from wagtail.snippets.models import register_snippet
from modelcluster.models import ClusterableModel

from .constants import DEFAULT_MAX_LENGTH

@register_snippet
class Theme(ClusterableModel):
    slug = models.SlugField()
    text = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    description = models.TextField()

    def __str__(self):
        return self.text

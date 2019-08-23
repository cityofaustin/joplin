from django.db import models

from modelcluster.models import ClusterableModel

from wagtail.snippets.models import register_snippet

@register_snippet
class Map(ClusterableModel):
    description = models.TextField()
    location = models.ForeignKey('base.Location', on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return self.description

    def serializable_data(self):
        data = {
            'location': self.location.serializable_data(),
            'description': self.description,
        }

        data['location'].pop('pk')

        return data

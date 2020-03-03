from django.db import models

from modelcluster.models import ClusterableModel

from wagtail.snippets.models import register_snippet


@register_snippet
class Map(ClusterableModel):
    description = models.TextField()
    location = models.ForeignKey('base.Location', on_delete=models.CASCADE, related_name='+')
    location_page = models.ForeignKey('locations.LocationPage', verbose_name='Select a Location', related_name='+', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.description

    def serializable_data(self):
        import pdb
        pdb.set_trace()
        # mapping location page to the data style of the snippet for backwards compatibility
        data = {
            'location': {
                'name': self.location_page.title,
                'street': self.location_page.physical_street,
                'city': self.location_page.physical_city,
                'state': self.location_page.physical_state,
                'country': self.location_page.physical_country,
                'zip': self.location_page.physical_zip
            },
            'description': self.description,
        }

        return data

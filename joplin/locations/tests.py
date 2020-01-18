from django.core.exceptions import ValidationError
from django.test import TestCase
from locations.models import LocationPageRelatedServices
from . import factories

class LocationPageTests(TestCase):
    def test_missing_related_service_hours_raises_error(self):
        location_page = factories.LocationPageFactory()
        try:
            location_page.full_clean()
        except ValidationError as e:
            self.assertRaises(ValidationError, instance.clean)

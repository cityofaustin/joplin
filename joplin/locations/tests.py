from django.core.validation import ValidationError
from django.test import TestCase
from locations.models import LocationPageRelatedServices
from locations import factories

class LocationPageRelatedServices(TestCase):

    def test_joe_must_have_a_website(self):
        p = Person(name='Joe', dob=datetime.date(1990, 1, 1))

        try:
            p.full_clean()
        except ValidationError as e:
            self.assertTrue('name' in e.message_dict)

instance = YourModel()
self.assertRaises(ValidationError, instance.clean)

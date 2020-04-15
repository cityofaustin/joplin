'''
    components.py contains elements that may be used
    interchangeably with multiple fixtures
'''
from pages.home_page.models import HomePage
import pages.location_page.fixtures as location_page_fixtures


def home():
    return HomePage.objects.first()


def city_location_block():
    location_page = location_page_fixtures.title()
    return [
        {
            "type": "city_location",
            "value": {
                "location_page": location_page.pk,
                "additional_details_en": "room 567",
                "additional_details_es": "",
                "additional_details_ar": "",
                "additional_details_vi": "",
            }
        }
    ]


# TODO
def remote_location_block():
    return []

'''
    components.py contains elements that may be used
    interchangeably with multiple fixtures
'''
from pages.home_page.models import HomePage
import pages.locations.fixtures as location_page_fixtures


def home():
    return HomePage.objects.first()


def city_location_block():
    location_page = location_page_fixtures.title()
    return [
      {
        "type": "city_location",
        "value": [
          {
            "type": "location_page",
            "value": location_page.pk,
          },
          {
            "type": "additional_details_en",
            "value": "room 567"
          },
          {
            "type": "additional_details_es",
            "value": ""
          },
          {
            "type": "additional_details_ar",
            "value": ""
          },
          {
            "type": "additional_details_vi",
            "value": ""
          }
        ]
      }
    ]


# TODO
def remote_location_block():
    return []

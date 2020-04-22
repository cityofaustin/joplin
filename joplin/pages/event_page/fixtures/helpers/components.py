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


def remote_location_block():
    return [
        {
            "type": "remote_location",
            "value": [
                {
                    "type": "name_en",
                    "value": "Faulk"
                },
                {
                    "type": "name_es",
                    "value": ''
                },
                {
                    "type": "name_ar",
                    "value": ''
                },
                {
                    "type": "name_vi",
                    "value": ''
                },
                {
                    "type": "street",
                    "value": "123 Fake St."
                },
                {
                    "type": "unit",
                    "value": ''
                },
                {
                    "type": "city",
                    "value": "Dallas"
                },
                {
                    "type": "state",
                    "value": "TX"
                },
                {
                    "type": "zip",
                    "value": "80389"
                },
                {
                    "type": "additional_details_en",
                    "value": "No."
                },
                {
                    "type": "additional_details_es",
                    "value": ''
                },
                {
                    "type": "additional_details_ar",
                    "value": ''
                },
                {
                    "type": "additional_details_vi",
                    "value": ''
                }
            ]
        }
    ]

three_fees = [
    {
        "fee": 0,
        "fee_label": "Kids"
    },
    {
        "fee": 5,
        "fee_label": "Adults"
    },
    {
        "fee": 20,
        "fee_label": "VIP"
    }
]

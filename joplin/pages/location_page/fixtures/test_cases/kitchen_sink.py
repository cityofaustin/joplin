import os
from pages.location_page.fixtures.helpers.create_fixture import create_fixture
import pages.location_page.fixtures.helpers.components as components


def kitchen_sink_page_data():
    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": components.home(),
        "coa_global": False,
        "title": "Kitchen sink location [en]",
        "slug": "kitchen-sink-location",
        'physical_street': '2514 Business Center Drive',
        'physical_unit': '',
        'physical_city': 'Austin',
        'physical_state': 'TX',
        'physical_zip': '78744'
    }

    return page_data


# A 'kitchen sink' location page
def kitchen_sink():
    return create_fixture(kitchen_sink_page_data(), os.path.basename(__file__))

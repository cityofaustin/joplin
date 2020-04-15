import os
from pages.service_page.fixtures.helpers.create_fixture import create_fixture
import pages.service_page.fixtures.helpers.components as components


# A Service Page that has a step with a location
def steps_with_location():
    page_data = {
        "imported_revision_id": None,
        "live": False,
        "parent": components.home(),
        "coa_global": False,
        "title": "Service Page with location step",
        "slug": "service-page-with-location-step",
        "add_topics": {
            "topics": []
        },
        "short_description": "This is a very short description",
        "additional_content": components.additional_content,
        "steps": components.steps_with_location,
    }

    return create_fixture(page_data, os.path.basename(__file__))

import os
from pages.service_page.fixtures.helpers.create_fixture import create_fixture
import pages.service_page.fixtures.helpers.components as components


# A Service Page that has a step with a location first followed by a basic step
def step_with_location_first_then_basic_step():
    steps = components.step_with_location_first_then_basic_step()
    home = components.home()
    page_data = {
        "imported_revision_id": None,
        "live": False,
        "parent": home,
        "coa_global": False,
        "title": "Service Page with location step followed by basic step",
        "slug": "service-page-with-location-basic-steps",
        "add_topics": {
            "topics": []
        },
        "short_description": "This is a very short description",
        "additional_content": components.additional_content,
        "steps": steps,
    }

    return create_fixture(page_data, os.path.basename(__file__))

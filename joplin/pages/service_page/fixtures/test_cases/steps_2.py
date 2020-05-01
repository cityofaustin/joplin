import os
from pages.service_page.fixtures.helpers.create_fixture import create_fixture
import pages.service_page.fixtures.helpers.components as components


# A fixture with 2 basic steps
def steps_2():
    page_data = {
        "imported_revision_id": None,
        "live": False,
        "parent": components.home(),
        "coa_global": False,
        "title": "Service Page with 2 Steps",
        "slug": "2-step-yee-haw",
        "add_topics": {
            "topics": []
        },
        "short_description": "This is a very short description",
        "additional_content": components.additional_content,
        "steps": components.steps_2,
    }

    return create_fixture(page_data, os.path.basename(__file__))

import os
from pages.service_page.fixtures.helpers.create_fixture import create_fixture
import pages.service_page.fixtures.helpers.components as components


# A fixture with 2 basic steps
def steps_2_live():
    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": components.home(),
        "coa_global": False,
        "title": "Service Page with 2 Steps Live",
        "slug": "2-step-yee-haw-live",
        "add_topics": {
            "topics": []
        },
        "short_description": "This is a very short description of a LIVE texas 2 step...",
        "dynamic_content": components.dynamic_content_list,
        "steps": components.steps_2,
    }

    return create_fixture(page_data, os.path.basename(__file__))

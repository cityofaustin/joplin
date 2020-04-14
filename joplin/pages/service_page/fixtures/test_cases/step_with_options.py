import os
from pages.service_page.fixtures.helpers.create_fixture import create_fixture
import pages.service_page.fixtures.helpers.components as components


# A fixture with a step with options
def step_with_options():
    page_data = {
        "imported_revision_id": None,
        "live": False,
        "parent": components.home(),
        "coa_global": False,
        "title": "Service Page with a Step with options",
        "slug": "step-with-yee-or-haw",
        "add_topics": {
            "topics": []
        },
        "short_description": "This is a very short description",
        "dynamic_content": components.dynamic_content,
        "steps": components.step_with_options,
    }

    return create_fixture(page_data, os.path.basename(__file__))

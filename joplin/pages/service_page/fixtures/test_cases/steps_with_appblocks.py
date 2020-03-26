import os
from pages.service_page.fixtures.helpers.create_fixture import create_fixture
import pages.service_page.fixtures.helpers.components as components


# A Service Page that has steps that contain Appblocks
def steps_with_appblocks():
    page_data = {
        "imported_revision_id": None,
        "live": False,
        "parent": components.home(),
        "coa_global": False,
        "title": "Service Page with Appblock steps",
        "slug": "service-page-appblocks",
        "add_topics": {
            "topics": []
        },
        "short_description": "This is a very short description",
        "dynamic_content": components.dynamic_content,
        "steps": components.steps_with_appblocks,
    }

    return create_fixture(page_data, os.path.basename(__file__))

import os
from pages.service_page.fixtures.helpers.create_fixture import create_fixture
import pages.service_page.fixtures.helpers.components as components


# A Service Page that has steps that contain Appblocks
def steps_with_appblocks_live():
    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": components.home(),
        "coa_global": False,
        "title": "Service Page with Appblock steps live",
        "slug": "service-page-appblocks-live",
        "add_topics": {
            "topics": []
        },
        "short_description": "This is a very short description of a LIVE appblock service page",
        "dynamic_content": components.dynamic_content_list,
        "steps": components.steps_with_appblocks,
    }

    return create_fixture(page_data, os.path.basename(__file__))

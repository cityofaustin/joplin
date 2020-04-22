import os
from pages.service_page.fixtures.helpers.create_fixture import create_fixture
import pages.service_page.fixtures.helpers.components as components


# A Service Page that has a step with internal links
def step_with_internal_links():
    steps = components.step_with_one_imported_and_some_unimported_internal_links()
    home = components.home()
    page_data = {
        "imported_revision_id": None,
        "live": False,
        "parent": home,
        "coa_global": False,
        "title": "Service Page with internal links",
        "slug": "service-page-with-internal-links",
        "add_topics": {
            "topics": []
        },
        "short_description": "This is a very short description",
        "additional_content": components.additional_content,
        "steps": steps,
    }

    return create_fixture(page_data, os.path.basename(__file__))

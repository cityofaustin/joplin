import os
from pages.department_page.fixtures.helpers.create_fixture import create_fixture
import pages.department_page.fixtures.helpers.components as components

# A "kitchen sink" department page
def kitchen_sink():
    page_data = {
        "imported_revision_id": None,
        "live": True,
        "published": True,
        "parent": components.home(),
        "title": "Kitchen sink department page [en]",
        "title_es": "Kitchen sink department page [es]",
        "slug": "kitchen-sink-department",
    }

    return create_fixture(page_data, os.path.basename(__file__))

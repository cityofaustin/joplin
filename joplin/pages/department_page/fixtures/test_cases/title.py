import os
from pages.department_page.fixtures.helpers.create_fixture import create_fixture
import pages.department_page.fixtures.helpers.components as components


# A department page with only a title
def title():
    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": components.home(),
        "coa_global": False,
        "title": "Department page with title",
        "slug": "department-page-with-title",
    }

    return create_fixture(page_data, os.path.basename(__file__))

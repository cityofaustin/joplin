import os
from pages.home_page.fixtures.helpers.create_fixture import create_fixture


# A HomePage page for use with our pytest janis branch
def pytest():
    page_data = {
        "publish_janis_branch": "pytest",
        "preview_janis_branch": "pytest",
        "slug": "pytest",
        "title": "pytest",
    }

    return create_fixture(page_data, os.path.basename(__file__))

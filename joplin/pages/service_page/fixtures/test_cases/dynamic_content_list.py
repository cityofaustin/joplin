import os
from pages.service_page.fixtures.helpers.create_fixture import create_fixture
import pages.service_page.fixtures.helpers.components as components


# A Service Page that has a list returned as dynamic_content
# for example: https://janis.austintexas.io/en/preview/services/UGFnZVJldmlzaW9uTm9kZTozNDA3
def dynamic_content_list():
    page_data = {
        "imported_revision_id": None,
        "live": False,
        "parent": components.home(),
        "coa_global": False,
        "title": "Service Page with dynamic content list",
        "slug": "service-page-dynamic-content-list",
        "add_topics": {
            "topics": []
        },
        "dynamic_content": components.dynamic_content_list,
    }

    return create_fixture(page_data, os.path.basename(__file__))

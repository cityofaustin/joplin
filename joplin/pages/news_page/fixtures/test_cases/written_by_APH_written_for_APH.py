import os
from pages.news_page.fixtures.helpers.create_fixture import create_fixture
import pages.news_page.fixtures.helpers.components as components
import snippets.contact.fixtures.helpers.components as contact_components
import pages.department_page.fixtures.helpers.components as department_page_components
from groups.fixtures.test_cases.mvp_news_aph import mvp_news_aph


def written_by_APH_written_for_APH():
    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": components.home(),
        "coa_global": False,
        "title": components.mvp_news_title,
        "slug": "mvp-news",
        "body": components.mvp_news_body,
        "written_for_department": department_page_components.mvp_news_aph(),
        "contact": contact_components.mvp_news_contact(),
        "add_departments": {
            "departments": [mvp_news_aph()]
        },
    }

    return create_fixture(page_data, os.path.basename(__file__))

import os
from pages.news_page.fixtures.helpers.create_fixture import create_fixture
import pages.news_page.fixtures.helpers.components as components
import snippets.contact.fixtures.helpers.components as contact_components
from groups.fixtures.test_cases.mvp_news_aph import mvp_news_aph


def written_by_APH():
    page_data = {
        "imported_revision_id": None,
        "live": True,
        "published": True,
        "parent": components.home(),
        "coa_global": False,
        "title": components.mvp_news_title,
        "title_es": components.google_translated_mvp_news_title,
        "slug": "mvp-news-by-aph",
        "body": components.mvp_news_body,
        "body_es": components.google_translated_mvp_news_body,
        "contact": contact_components.mvp_news_contact(),
        "add_departments": {
            "departments": [mvp_news_aph()]
        },
    }

    return create_fixture(page_data, os.path.basename(__file__))

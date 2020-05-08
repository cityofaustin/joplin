'''
    components.py contains elements that may be used
    interchangeably with multiple fixtures
'''
from pages.home_page.models import HomePage
from pages.department_page.fixtures.helpers.create_fixture import create_fixture
import os


def home():
    return HomePage.objects.first()


# A department page to represent APH for our MVP news test data
# https://share.goabstract.com/ac28fbf0-0ef7-448c-98d7-b652d936a2f8
def mvp_news_aph():
    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": home(),
        "title": "Austin Public Health",
        "title_es": "Salud Pública de Austin",
        "slug": "mvp-news-aph",
    }

    return create_fixture(page_data, os.path.basename(__file__))


# same thing as aph above but for CPIO
def mvp_news_cpio():
    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": home(),
        "title": "Communications and Public Information Office",
        "slug": "mvp-news-cpio",
    }

    return create_fixture(page_data, os.path.basename(__file__))


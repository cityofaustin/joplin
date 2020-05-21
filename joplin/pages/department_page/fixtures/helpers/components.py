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
        "what_we_do": "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed dignissim purus in elementum consequat. Nam vestibulum feugiat faucibus. Donec consequat massa sed neque semper sodales. Vivamus molestie consequat dictum. Nam elit nisi, auctor pulvinar mi vestibulum, dignissim commodo nunc. Aenean in tempor nunc. Mauris tempus sem ultrices nisl consectetur convallis. Aliquam erat volutpat. Morbi ut ipsum placerat, porta eros a, volutpat eros. Aenean rhoncus leo in cursus interdum. Cras ac sem metus. Proin ultrices neque massa, id placerat sapien pulvinar ac. Integer nec dapibus lacus, id porta odio. Fusce lobortis tempor tempus. Duis quis dignissim leo, nec gravida tortor. Aenean non accumsan diam, eu dapibus erat.</p>",
        "mission": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed dignissim purus in elementum consequat. Nam vestibulum feugiat faucibus. Donec consequat massa sed neque semper sodales. Vivamus molestie consequat dictum. Nam elit nisi, auctor pulvinar mi vestibulum, dignissim commodo nunc. Aenean in tempor nunc. Mauris tempus sem ultrices nisl consectetur convallis. Aliquam erat volutpat.",
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


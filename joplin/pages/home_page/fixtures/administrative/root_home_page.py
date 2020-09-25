import os
from pages.home_page.models import HomePage
from pages.home_page.fixtures.helpers.create_fixture import create_fixture
from wagtail.core.models import Site


# This is our root level HomePage.
# We used to run this home_page creation script in a migration, but then weird bugs happened with model_translation.
def root_home_page():
    try:
        home = HomePage.objects.get(slug='home')
    except HomePage.DoesNotExist:
        home = HomePage.objects.create(
            title="Home",
            draft_title="Home",
            slug='home',
            path='00010001',
            depth=2,
            numchild=0,
            url_path='/home/',
        )

        Site.objects.create(
            hostname='localhost', port=80, root_page=home, is_default_site=True
        )

    return home

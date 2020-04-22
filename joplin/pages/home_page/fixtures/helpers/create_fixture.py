from pages.home_page.models import HomePage
from pages.home_page.factories import HomePageFactory


# Skips creating fixture if Page with slug already exists
def create_fixture(page_data, fixture_name):
    try:
        page = HomePage.objects.get(slug=page_data['slug'])
    except HomePage.DoesNotExist:
        page = None
    if page:
        print(f"Skipping {fixture_name}")
        return None

    page = HomePageFactory.create(**page_data)
    print(f"Built {fixture_name}")
    return page

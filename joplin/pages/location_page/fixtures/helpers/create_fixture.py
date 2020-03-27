from pages.location_page.models import LocationPage
from pages.location_page.factories import LocationPageFactory


# Skips creating fixture if Page with slug already exists
def create_fixture(page_data, fixture_name):
    try:
        page = LocationPage.objects.get(slug=page_data['slug'])
    except LocationPage.DoesNotExist:
        page = None
    if page:
        print(f"Skipping {fixture_name}")
        return None

    page = LocationPageFactory.create(**page_data)
    print(f"Built {fixture_name}")
    return page

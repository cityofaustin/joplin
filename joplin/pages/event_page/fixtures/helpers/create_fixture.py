from pages.event_page.models import EventPage
from pages.event_page.factories import EventPageFactory


# Skips creating fixture if Page with slug already exists
def create_fixture(page_data, fixture_name):
    try:
        page = EventPage.objects.get(slug=page_data['slug'])
    except EventPage.DoesNotExist:
        page = None
    if page:
        print(f"Skipping {fixture_name}")
        return None

    page = EventPageFactory.create(**page_data)
    print(f"Built {fixture_name}")
    return page

from pages.service_page.models import ServicePage
from pages.service_page.factories import ServicePageFactory


# Skips creating fixture if Page with slug already exists
def create_fixture(page_data, fixture_name):
    try:
        page = ServicePage.objects.get(slug=page_data['slug'])
    except ServicePage.DoesNotExist:
        page = None
    if page:
        print(f"Skipping service page fixture: {fixture_name}")
        return None

    page = ServicePageFactory.create(**page_data)
    print(f"Built service page fixture: {fixture_name}")
    return page

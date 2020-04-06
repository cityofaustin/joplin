from pages.information_page.models import InformationPage
from pages.information_page.factories import InformationPageFactory


# Skips creating fixture if Page with slug already exists
def create_fixture(page_data, fixture_name):
    try:
        page = InformationPage.objects.get(slug=page_data['slug'])
    except InformationPage.DoesNotExist:
        page = None
    if page:
        print(f"Skipping {fixture_name}")
        return None

    page = InformationPageFactory.create(**page_data)
    print(f"Built {fixture_name}")
    return page

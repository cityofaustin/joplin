from pages.official_documents_page.models import OfficialDocumentPage
from pages.official_documents_page.factories import OfficialDocumentPageFactory


# Skips creating fixture if Page with slug already exists
def create_fixture(page_data, fixture_name):
    try:
        page = OfficialDocumentPage.objects.get(slug=page_data['slug'])
    except OfficialDocumentPage.DoesNotExist:
        page = None
    if page:
        print(f"Skipping topic page fixture: {fixture_name}")
        return page

    page = OfficialDocumentPageFactory.create(**page_data)
    print(f"Built topic page fixture: {fixture_name}")
    return page

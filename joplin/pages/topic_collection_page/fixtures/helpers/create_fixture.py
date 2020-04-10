from pages.topic_collection_page.models import TopicCollectionPage
from pages.topic_collection_page.factories import TopicCollectionPageFactory


# Skips creating fixture if Page with slug already exists
def create_fixture(page_data, fixture_name):
    try:
        page = TopicCollectionPage.objects.get(slug=page_data['slug'])
    except TopicCollectionPage.DoesNotExist:
        page = None
    if page:
        print(f"Skipping topic collection page fixture: {fixture_name}")
        return None

    page = TopicCollectionPageFactory.create(**page_data)
    print(f"Built topic collection page fixture: {fixture_name}")
    return page

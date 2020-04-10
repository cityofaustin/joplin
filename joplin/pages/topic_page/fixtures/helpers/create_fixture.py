from pages.topic_page.models import TopicPage
from pages.topic_page.factories import TopicPageFactory


# Skips creating fixture if Page with slug already exists
def create_fixture(page_data, fixture_name):
    try:
        page = TopicPage.objects.get(slug=page_data['slug'])
    except TopicPage.DoesNotExist:
        page = None
    if page:
        print(f"Skipping topic page fixture: {fixture_name}")
        return None

    page = TopicPageFactory.create(**page_data)
    print(f"Built topic page fixture: {fixture_name}")
    return page

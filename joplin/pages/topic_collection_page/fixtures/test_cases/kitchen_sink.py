import os
from pages.topic_collection_page.fixtures.helpers.create_fixture import create_fixture
import pages.topic_collection_page.fixtures.helpers.components as components
from snippets.theme.fixtures.test_cases import kitchen_sink as kitchen_sink_theme

# A "kitchen sink" topic collection page
def kitchen_sink():
    theme = kitchen_sink_theme.kitchen_sink()

    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": components.home(),
        "title": "Kitchen sink topic collection page [en]",
        "title_es": "Kitchen sink topic collection page [es]",
        "slug": "kitchen-sink-topic-collection-page",
        "theme": theme
    }

    return create_fixture(page_data, os.path.basename(__file__))

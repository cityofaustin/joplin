import os
from pages.topic_page.fixtures.helpers.create_fixture import create_fixture
import pages.topic_page.fixtures.helpers.components as components
from pages.topic_collection_page.fixtures.test_cases import kitchen_sink as kitchen_sink_topic_collection


# A topic page with a title
def title():
    topic_collection = kitchen_sink_topic_collection.kitchen_sink()

    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": components.home(),
        "title": "Topic title [en]",
        "title_es": "Topic title [es]",
        "slug": "topic-title-en",
        "add_topic_collections": {
            "topic_collections": [topic_collection]
        },
    }

    return create_fixture(page_data, os.path.basename(__file__))

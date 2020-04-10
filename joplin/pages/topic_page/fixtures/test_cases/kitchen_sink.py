import os
from pages.topic_page.fixtures.helpers.create_fixture import create_fixture
import pages.topic_page.fixtures.helpers.components as components
from pages.topic_collection_page.fixtures.test_cases import kitchen_sink as kitchen_sink_topic_collection

# A "kitchen sink" topic page
def kitchen_sink():
    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": components.home(),
        "title": "Kitchen sink topic page [en]",
        "title_es": "Kitchen sink topic page [es]",
        "slug": "kitchen-sink-topic-page",
        "add_topic_collections": {
            "topic_collections": [kitchen_sink_topic_collection.kitchen_sink()]
        },
    }

    return create_fixture(page_data, os.path.basename(__file__))

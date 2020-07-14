import os
from pages.official_documents_collection.fixtures.helpers.create_fixture import create_fixture
import pages.official_documents_collection.fixtures.helpers.components as components
from pages.topic_page.fixtures.test_cases import kitchen_sink as kitchen_sink_topic


# A "kitchen sink" official documents collection
def kitchen_sink():
    topic = kitchen_sink_topic.kitchen_sink()

    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": components.home(),
        "coa_global": False,
        "title": "Kitchen sink official documents page [en]",
        "title_es": "Kitchen sink official documents page [es]",
        "slug": "kitchen-sink-official-documents-collection",
        "add_topics": {
            "topics": [topic]
        },
        "description": "Kitchen sink official documents list description [en]",
        "description_es": "Kitchen sink official documents list description [es]",
    }

    return create_fixture(page_data, os.path.basename(__file__))

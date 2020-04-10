import hashlib
import os
from pages.official_documents_page.fixtures.helpers.create_fixture import create_fixture, create_fixture_document
import pages.official_documents_page.fixtures.helpers.components as components
from pages.topic_page.fixtures.test_cases import kitchen_sink as kitchen_sink_topic


# A "kitchen sink" official documents page
def kitchen_sink():
    topic = kitchen_sink_topic.kitchen_sink()

    # add a document
    file_name = 'filename.txt'
    file_content = "I am file content"
    document = create_fixture_document(file_content, file_name)
    official_documents_page_document_node = {
        'date': "1/1/2021",
        'document': document
    }

    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": components.home(),
        "coa_global": False,
        "title": "Kitchen sink official documents page [en]",
        "title_es": "Kitchen sink official documents page [es]",
        "slug": "kitchen-sink-official-documents-page",
        "add_topics": {
            "topics": [topic]
        },
        "description": "Kitchen sink official documents page description [en]",
        "description_es": "Kitchen sink official documents page description [es]",
        'add_official_documents_page_documents': {'official_documents_page_documents': [official_documents_page_document_node]}
    }

    return create_fixture(page_data, os.path.basename(__file__))

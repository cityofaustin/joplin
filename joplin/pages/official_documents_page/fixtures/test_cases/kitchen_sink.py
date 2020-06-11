import hashlib
import os
from pages.official_documents_page.fixtures.helpers.create_fixture import create_fixture, create_fixture_document
import pages.official_documents_page.fixtures.helpers.components as components
from pages.topic_page.fixtures.test_cases import kitchen_sink as kitchen_sink_topic


# A "kitchen sink" official documents page
def kitchen_sink():
    topic = kitchen_sink_topic.kitchen_sink()

    # add a document
    file_name = 'kitchen-sink-file-en.txt'
    file_name_es = 'kitchen-sink-file-es.txt'
    file_content = str("I am file content [en]").encode('utf-8')
    file_content_es = str("I am file content [es]").encode('utf-8')
    document = create_fixture_document(file_content, file_name)
    document_es = create_fixture_document(file_content_es, file_name_es)


    official_documents_page_document_node = {
        'date': "2021-01-01",
        'document': document,
        'document_es': document_es,
        'title': 'Kitchen sink document title [en]',
        'title_es': 'Kitchen sink document title [es]',
        'authoring_office': 'Kitchen sink document authoring office [en]',
        'authoring_office_es': 'Kitchen sink document authoring office [es]',
        'summary': 'Kitchen sink document summary [en]',
        'summary_es': 'Kitchen sink document summary [es]',
        'name': 'Kitchen sink document name [en]',
        'name_es': 'Kitchen sink document name [es]',
    }

    page_data = {
        "imported_revision_id": None,
        "live": True,
        "published": True,
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

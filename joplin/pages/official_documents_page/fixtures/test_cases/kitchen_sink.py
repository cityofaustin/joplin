import os
from pages.official_documents_page.fixtures.helpers.create_fixture import create_fixture, create_fixture_document
import pages.official_documents_page.fixtures.helpers.components as components
from pages.official_documents_list.fixtures.test_cases import kitchen_sink as kitchen_sink_official_documents_list


# A "kitchen sink" official documents page
def kitchen_sink():
    official_documents_list = kitchen_sink_official_documents_list.kitchen_sink()

    # add a document
    file_name = 'kitchen-sink-file-en.txt'
    file_name_es = 'kitchen-sink-file-es.txt'
    file_content = str("I am file content [en]").encode('utf-8')
    file_content_es = str("I am file content [es]").encode('utf-8')
    document = create_fixture_document(file_content, file_name)
    document_es = create_fixture_document(file_content_es, file_name_es)

    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": components.home(),
        "coa_global": False,
        "title": "Kitchen sink official documents page [en]",
        "title_es": "Kitchen sink official documents page [es]",
        "slug": "kitchen-sink-official-documents-page",
        'date': "2021-01-01",
        'document': document,
        'document_es': document_es,
        'document_title': 'Kitchen sink document title [en]',
        'document_title_es': 'Kitchen sink document title [es]',
        'authoring_office': 'Kitchen sink document authoring office [en]',
        'authoring_office_es': 'Kitchen sink document authoring office [es]',
        'summary': 'Kitchen sink document summary [en]',
        'summary_es': 'Kitchen sink document summary [es]',
        'name': 'Kitchen sink document name [en]',
        'name_es': 'Kitchen sink document name [es]',
        'add_official_documents_list': {'official_documents_list': [official_documents_list]}
    }

    return create_fixture(page_data, os.path.basename(__file__))

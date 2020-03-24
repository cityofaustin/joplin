import pytest

from importer.page_importer import PageImporter
from pages.topic_collection_page.factories import ThemeFactory, TopicCollectionPageFactory, \
    create_topic_collection_page_from_page_dictionary
from pages.topic_page.factories import TopicPageFactory, create_topic_page_from_page_dictionary
from pages.service_page.factories import ServicePageFactory, create_service_page_from_page_dictionary




from pytest_factoryboy import register
import pytest
import inspect
from factory.base import FactoryMetaClass
from pages.information_page import factories as information_page_factories
from pages.official_documents_page import factories as official_document_page_factories
from pages.department_page import factories as department_page_factories
# from pages.
# from base.factories import service_page, guide_page


from django.core.management import call_command


# @pytest.fixture(scope='session')
# def django_db_setup(django_db_setup, django_db_blocker):
#     """
#     uses pytest-django to load data into a pytest fixture
#     this populates the test database
#     tests that are decoratored accordingly will use the db
#     eventually we'll want to make our factories robust and rely on a test db
#     as little possible, but this is a handy stop-gap
#     """
#     # with django_db_blocker.unblock():
#         # this is definitely not working right now
#         # call_command('loaddata', 'joplin/db/system-generated/prod.datadump.json')


def register_factories(factories):
    """
    lil loop to go through and register factory objects
    like this:
    register(InformationPageContactFactory)
    register(InformationPageFactory)
    but without having to write them all out
    """
    for name, object in inspect.getmembers(factories):
        if isinstance(object, FactoryMetaClass) and not object._meta.abstract:
            register(object)


# register_factories(information_page_factories)
# register_factories(department_page_factories)
register_factories(official_document_page_factories)
# register_factories(service_page)
# register_factories(guide_page)

# example if we wanted to make a specific fixture for some tests, we can flesh
# this out with specific names or parameters, good for regression tests
# TODO: example like 'page without topic'
# @pytest.fixture()
# def information_page(information_page_factory):
#     return InformationPageFactory.build()

from pytest_factoryboy import register
import pytest
import inspect
from factory.base import FactoryMetaClass
from pages.information_page import factories as information_page_factories
from pages.official_documents_page import factories as official_document_page_factories
from pages.department_page import factories as department_page_factories
import pages.home_page.fixtures as home_page_fixtures


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


'''
Fixtures created in conftest.py can be used in any test without importing.
https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions
'''
@pytest.fixture()
def remote_pytest_api():
    return 'https://joplin-pr-pytest.herokuapp.com/api/graphql'


# TODO: Once preview urls work on Janis with v3, then we can use this URL
@pytest.fixture()
def remote_pytest_preview_url():
    return 'https://janis-pytest.netlify.com/en/preview'


@pytest.fixture()
def remote_staging_preview_url():
    return 'https://janis.austintexas.io/en/preview'


@pytest.fixture()
def home_page():
    return home_page_fixtures.pytest()


@pytest.fixture()
def expected_publish_url_base():
    return "https://janis-v3-pytest.netlify.app"

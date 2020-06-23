from pytest_factoryboy import register
import pytest
import inspect
import os
from factory.base import FactoryMetaClass
import json
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

import pages.home_page.fixtures as home_page_fixtures
import base.fixtures.administrative.mandatory_fixtures as mandatory_fixtures

# from django.core.management import call_command
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


# Genius technique from: https://stackoverflow.com/questions/42652228/removing-cached-files-after-a-py-test-run
@pytest.yield_fixture(autouse=True, scope='session')
def test_suite_cleanup_thing(request):
    # Setup: Everything before yield will happen at the beginning of your pytest session

    # Clear test_api_jwt_token at start of running entire test suite.
    # This will ensure that our test_api_jwt_token is only cached for 1 pytest invocation and won't expire.
    request.config.cache.set('test_api_jwt_token', None)
    yield
    # Teardown: Everything after yield will happen at the end of your pytest session

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
def test_api_url():
    return 'https://joplin-pr-pytest.herokuapp.com/api/graphql'


@pytest.fixture()
def test_api_jwt_token(request, test_api_url):
    # Requesting the jwt_token takes a long time.
    # So we'll put it in the cache once we've retrieved it once for this session.
    jwt_token = request.config.cache.get('test_api_jwt_token', None)
    if jwt_token:
        return jwt_token
    transport = RequestsHTTPTransport(
        url=test_api_url,
        headers={
            'Accept-Language': 'en',
        },
        verify=False,
        retries=3,
    )
    client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )
    jwt_token_query = gql('''
        mutation TokenAuth($email: String!, $password: String!) {
          tokenAuth(email: $email, password: $password) {
            token
          }
        }
    ''')
    result = client.execute(jwt_token_query, variable_values=json.dumps({
        'email': "apitest@austintexas.io",
        'password': os.getenv("API_TEST_USER_PASSWORD"),
    }))
    jwt_token = result['tokenAuth']['token']
    request.config.cache.set('test_api_jwt_token', jwt_token)
    return jwt_token


# TODO: Once preview urls work on Janis with v3, then we can use this URL
@pytest.fixture()
def remote_pytest_preview_url():
    return 'https://janis-pytest.netlify.com/en/preview'


# TODO: All importer tests should be conducted on pytest
@pytest.fixture()
def remote_staging_preview_url():
    return 'https://janis.austintexas.io/en/preview'


@pytest.fixture()
def home_page():
    return home_page_fixtures.pytest()


@pytest.fixture()
def expected_publish_url_base():
    return "https://janis-v3-pytest.netlify.com"

import os
from gql.transport.requests import RequestsHTTPTransport
from gql import Client
from gql import gql
from importer.queries import queries
import json
from importer.page_importer import PageImporter
from pages.base_page.models import JanisBasePage

api_url = 'http://joplin.herokuapp.com/api/graphql'
page_type_map = {
    'service page': 'services',
    'guide page': None,
    'topic collection page': 'topiccollection',
    'information page': 'information',
    'department page': 'department',
    'form container': 'form',
    'topic page': 'topic',
    'official document page': 'official_document',
    'event page': 'event',
    'location page': 'location'
}


def get_jwt_token():
    transport = RequestsHTTPTransport(
        url=api_url,
        headers={
            'Accept-Language': 'en',
        },
        verify=True
    )
    client = Client(
        retries=3,
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
        'email': "admin@austintexas.io",
        'password': os.getenv("IMPORTER_USER_PASSWORD"),
    }))
    jwt_token = result['tokenAuth']['token']
    return jwt_token


def fetch_revision_ids(jwt_token):
    sample_transport = RequestsHTTPTransport(
        url=api_url,
        headers={
            'Accept-Language': 'en',
            'Authorization': u'JWT {0}'.format(jwt_token),
        },
        verify=True
    )

    client = Client(
        retries=3,
        transport=sample_transport,
        fetch_schema_from_transport=True,
    )

    all_page_revisions = []
    after_cursor = ''
    has_next_page = True
    while has_next_page:
        result = client.execute(queries['all_revisions'], variable_values=json.dumps({'afterCursor': after_cursor}))
        after_cursor = result['allPageRevisions']['pageInfo']['endCursor']
        has_next_page = result['allPageRevisions']['pageInfo']['hasNextPage']
        all_page_revisions.extend(result['allPageRevisions']['edges'])

    return all_page_revisions


def import_page_from_revision(revision, jwt_token):
    try:
        # If we have already imported this revision, skip it
        page = JanisBasePage.objects.get(imported_revision_id=revision['node']['id'])

        # if we have already imported this live revision and the page hasn't gone live
        if not page.live and revision['node']['isLive']:
            # make a note of it todo: figure out updating
            print(u'Page to manually check: {0}'.format(page.title))

        print(u'Page revision {0} already imported, skipping...'.format(page.imported_revision_id))
    except JanisBasePage.DoesNotExist:
        # If we haven't already imported this revision, import it
        page_importer = PageImporter(u'?CMS_API={0}'.format(api_url), jwt_token)
        page_importer.revision_id = revision['node']['id']
        page_importer.page_type = page_type_map[revision['node']['pageType']]
        if page_importer.page_type:
            print(
                u'Found {0} revision {1}, importing...'.format(revision['node']['pageType'], page_importer.revision_id))
            try:
                page = page_importer.fetch_page_data().create_page()
                print(u'Imported page: {0}'.format(page.title))
            except Exception as ex:
                print(u'FAILED to import {0} revision: {1}'.format(page_importer.page_type, page_importer.revision_id))
                print(ex)


def import_everything():
    jwt_token = get_jwt_token()
    all_page_revisions = fetch_revision_ids(jwt_token)

    latest_revisions = list(filter(lambda edge: edge['node']['isLatest'], all_page_revisions))

    # as per the logic in https://github.com/cityofaustin/joplin/pull/693
    # "For an ideal full site import, just make sure we import all location_pages before importing all service_pages."
    location_page_revisions = list(filter(lambda edge: edge['node']['pageType'] == 'location page', latest_revisions))
    for location_page_revision in location_page_revisions:
        import_page_from_revision(location_page_revision, jwt_token)

    for revision in latest_revisions:
        import_page_from_revision(revision, jwt_token)





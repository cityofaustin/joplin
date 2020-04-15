from gql.transport.requests import RequestsHTTPTransport
from gql import Client
from importer.queries import queries
import json
from importer.page_importer import PageImporter

jwt_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFkbWluQGF1c3RpbnRleGFzLmlvIiwiZXhwIjoxNTg2ODczMjQyLCJvcmlnSWF0IjoxNTg2ODcyOTQyfQ.fDss8txeS0Oe-OWeB3WiayV3vDhs-tCJLqQa0jpDuQM'
api_url = 'http://joplin-pr-latest-revision.herokuapp.com/api/graphql'
page_type_map = {
    'service page': 'services',
    'guide page': None,
    'topic collection page': 'topiccollection',
    'information page': 'information',
    'department page': 'department',
    'form container': 'form',
    'topic page': 'topic',
    'official document page': 'official_document',
    'event page': None,
    'location page': 'location'
}

def fetch_and_save_revision_ids():
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

    with open('third_revision_ids_file.json', 'w') as revision_ids_file:
        revision_ids_file.write(json.dumps(all_page_revisions))

def import_everything():
    # if we don't have a revision_ids_file then let's make one
    if False:
        fetch_and_save_revision_ids()

    latest_revisions = []
    with open('third_revision_ids_file.json') as revision_ids_file:
        all_page_revisions = json.load(revision_ids_file)
        latest_revisions = list(filter(lambda edge: edge['node']['isLatest'], all_page_revisions))

    for revision in latest_revisions:
        page_importer = PageImporter(u'?CMS_API={0}'.format(api_url), jwt_token)
        page_importer.revision_id = revision['node']['id']
        page_importer.page_type = page_type_map[revision['node']['pageType']]
        if page_importer.page_type:
            try:
                page = page_importer.fetch_page_data().create_page()
                print(u'Imported page: {0}'.format(page.title))
            except Exception as ex:
                print(u'FAILED to import page: {0}'.format(page.title))
                print(ex)





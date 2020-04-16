import os
from gql.transport.requests import RequestsHTTPTransport
from gql import Client
from gql import gql
from importer.queries import queries
import json
from importer.page_importer import PageImporter

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
        'password': 'x',
        # 🌵
        # 'password': u'{0}'.format(os.getenv("IMPORTER_USER_PASSWORD")),
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

    # with open('third_revision_ids_file.json', 'w') as revision_ids_file:
    #     revision_ids_file.write(json.dumps(all_page_revisions))

def import_everything():
    jwt_token = get_jwt_token()
    all_page_revisions = fetch_revision_ids(jwt_token)

    latest_revisions = list(filter(lambda edge: edge['node']['isLatest'], all_page_revisions))
    # with open('third_revision_ids_file.json') as revision_ids_file:
    #     all_page_revisions = json.load(revision_ids_file)
    #     latest_revisions = list(filter(lambda edge: edge['node']['isLatest'], all_page_revisions))

    for revision in latest_revisions:
        page_importer = PageImporter(u'?CMS_API={0}'.format(api_url), jwt_token)
        page_importer.revision_id = revision['node']['id']
        page_importer.page_type = page_type_map[revision['node']['pageType']]
        if page_importer.page_type:
            try:
                # if page_importer.revision_id == 'UGFnZVJldmlzaW9uTm9kZToxODY1':
                #     blarg = 3
                page = page_importer.fetch_page_data().create_page()
                print(u'Imported page: {0}'.format(page.title))
            except Exception as ex:
                print(u'FAILED to import page: {0}'.format(page.title))
                print(ex)





from gql.transport.requests import RequestsHTTPTransport
from gql import Client
from importer.queries import queries
import json

def fetch_and_save_revision_ids():
    sample_transport = RequestsHTTPTransport(
        url='http://joplin-pr-latest-revision.herokuapp.com/api/graphql',
        headers={
            'Accept-Language': 'en',
            'Authorization': f'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFkbWluQGF1c3RpbnRleGFzLmlvIiwiZXhwIjoxNTg2ODczMjQyLCJvcmlnSWF0IjoxNTg2ODcyOTQyfQ.fDss8txeS0Oe-OWeB3WiayV3vDhs-tCJLqQa0jpDuQM',
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

    with open('revision_ids_file.json', 'w') as revision_ids_file:
        revision_ids_file.write(json.dumps(all_page_revisions))

def import_everything():
    # if we don't have a revision_ids_file then let's make one
    if True:
        fetch_and_save_revision_ids()

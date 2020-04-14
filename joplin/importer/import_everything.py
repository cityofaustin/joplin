from gql.transport.requests import RequestsHTTPTransport
from gql import Client
from importer.queries import queries
import json

def import_everything():
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
    r = 0
    while has_next_page:
        result = client.execute(queries['all_revisions'], variable_values=json.dumps({'after_cursor': after_cursor}))
        after_cursor = result['allPageRevisions']['pageInfo']['endCursor']
        has_next_page = result['allPageRevisions']['pageInfo']['hasNextPage']
        all_page_revisions.extend(result['allPageRevisions']['edges'])
        r += 1
        print(u'got {0}'.format(100*r))
        if r == 20:
            has_next_page = False

    # todo: write this out to a file
    blarg = 3

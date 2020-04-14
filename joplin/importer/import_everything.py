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

    result = client.execute(queries['all_revisions'])

    blarg = 3

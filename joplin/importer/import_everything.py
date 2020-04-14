from gql.transport.requests import RequestsHTTPTransport


def import_everything():
    sample_transport = RequestsHTTPTransport(
        url='http://joplin-pr-latest-revision.herokuapp.com/api/graphql',
        headers={
            'Accept-Language': lang,
            'Authorization': f'JWT {self.jwt_token}',
        },
        verify=True
    )

    client = Client(
        retries=3,
        transport=sample_transport,
        fetch_schema_from_transport=True,
    )

    result = client.execute(queries[self.page_type], variable_values=json.dumps({'id': self.revision_id}))

    blarg = 3

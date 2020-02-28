import json

from graphene_django.utils.testing import GraphQLTestCase
from api.schema import schema
from graphene.test import Client
import pytest

servicePageQuery = '''
{
  allServicePages {
    edges {
      node {
        id
      }
    }
  }
}
'''


@pytest.mark.django_db
def test_service(snapshot):
    client = Client(schema)
    # This will create a snapshot dir and a snapshot file
    # the first time the test is executed, with the response
    # of the execution.
    snapshot.assert_match(client.execute(servicePageQuery))


class ResponseTestCase(GraphQLTestCase):
    # Here you need to inject your test case's schema
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = '/api/graphql'

    def test_query(self):
        response = self.query(servicePageQuery)
        content = json.loads(response.content)
        import pdb
        pdb.set_trace()
        self.assertResponseNoErrors(response)

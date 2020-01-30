import json

from graphene_django.utils.testing import GraphQLTestCase
from .schema import schema


class ResponseTestCase(GraphQLTestCase):
    # Here you need to inject your test case's schema
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = '/api/graphql'

    def test_query(self):
        response = self.query(
            '''
            {
              allServicePages{
                edges {
                  node {
                    title
                    id
                    steps {
                      value
                      stepType
                      locations {
                        value
                      }
                    }
                  }
                }
              }
            }
            '''
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

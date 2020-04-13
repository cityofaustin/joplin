# todo: figure out why something is breaking in here

# import json
#
# from graphene_django.utils.testing import GraphQLTestCase
# from api.schema import schema
# from graphene.test import Client
# import pytest
#
# servicePageQuery = '''
# {
#   allServicePages {
#     edges {
#       node {
#         id
#         title
#       }
#     }
#   }
# }
# '''
#
# informationPageQuery = '''
# {
#   allInformationPages {
#     edges {
#       node {
#         id
#         title
#       }
#     }
#   }
# }
# '''
#
#
# @pytest.mark.django_db
# def test_service(snapshot):
#     client = Client(schema)
#     # This will create a snapshot dir and a snapshot file
#     # the first time the test is executed, with the response
#     # of the execution.
#     snapshot.assert_match(client.execute(servicePageQuery))
#
#
# @pytest.mark.django_db
# def test_information(snapshot):
#     client = Client(schema)
#     # This will create a snapshot dir and a snapshot file
#     # the first time the test is executed, with the response
#     # of the execution.
#     snapshot.assert_match(client.execute(informationPageQuery))
#
#
# # example using graphql test case
# class ResponseTestCase(GraphQLTestCase):
#     # Here you need to inject your test case's schema
#     GRAPHQL_SCHEMA = schema
#     GRAPHQL_URL = '/api/graphql'
#
#     def test_query(self):
#         response = self.query(servicePageQuery)
#         content = json.loads(response.content)
#         # do other assertions on content here or in other methods if you want
#         self.assertIn('data', content.keys())
#         self.assertResponseNoErrors(response)
#
# # example using pytest, pretty sure this does basically the same thing
# @pytest.mark.django_db
# def test_service_query_has_data():
#     client = Client(schema)
#     content = client.execute(servicePageQuery)
#     assert 'data' in content.keys()

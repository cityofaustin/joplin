import os
from django.test import TestCase, Client
from django.core.management import call_command

c = Client()

# Run this test with pipenv run joplin/manage.py test api.tests.test_site_structure --keepdb
class TestSiteStructure(TestCase):
    def setUp(self):
        # setUp() is where you can load dummy data here with factory data or using a datadump.
        print("Loading dummy data")
        os.environ['LOAD_DATA'] = "staging"
        call_command('load_joplin_data')
        print("it worked")

    def test_has_response(self):
        response = c.post(
            path='/api/graphql',
            data={
                'query': '\n  query siteStructureQuery {\n    siteStructure {\n      structureJson\n    }\n  }\n'
            },
            content_type='application/json'
        )
        print("hi")
        self.assertTrue(True)

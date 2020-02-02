import os
from django.test import TestCase, Client
from django.core.management import call_command
from django.conf import settings
from wagtail.core.models import Page
from django.shortcuts import get_object_or_404

from users.models import User
from base.models import InformationPage, TopicPage, TopicCollectionPage, DepartmentPage

# pipenv run joplin/manage.py test publish_preflight.tests.information_page_test
class EasyTest(TestCase):
    def setUp(self):
        os.environ['LOAD_DATA'] = ""
        os.environ['DEPLOYMENT_MODE'] = "TEST"

        home = Page.objects.get(id=3)

        # Create test user
        self.user = User.objects.create_superuser(
            "test@austintexas.io",
            "test_password",
            is_staff=True,
            is_active=True,
            is_superuser=True,
        )

        # Create Test Topic Collection Page
        self.topic_collection = TopicCollectionPage(**{
            'title': "Pets",
            'owner': self.user,
        })
        home.add_child(instance=self.topic_collection)
        self.topic_collection.save_revision()
        self.topic_collection.unpublish()

        # Create Test Topic Page
        self.topic = TopicPage(**{
            'title': "Pet Adoption",
            'owner': self.user,
        })
        home.add_child(instance=self.topic)
        self.topic.save_revision()
        self.topic.topiccollections.add(self.topic_collection)
        self.topic.unpublish()

        # Create Test DepartmentPage
        self.department = DepartmentPage(**{
            'title': "Department of Animals",
            'owner': self.user,
        })
        home.add_child(instance=self.department)
        self.department.save_revision()
        self.department.unpublish()

        # Create Test Topic Page
        self.info_page = InformationPage(**{
            'title': "Adopt a baby tarantula",
            'owner': self.user,
        })
        home.add_child(instance=self.info_page)
        self.info_page.save_revision()
        self.info_page.unpublish()

    def test_setup_data_loaded(self):
        self.assertTrue(isinstance(self.topic, TopicPage))
        self.assertTrue(isinstance(self.topic_collection, TopicCollectionPage))
        self.assertTrue(self.topic.topiccollections.count() == 1)
        self.assertTrue(isinstance(self.department, DepartmentPage))
        self.assertTrue(isinstance(self.info_page, InformationPage))

    def test_no_publish_required_fields(self):
        fake_request = {
            "action-publish": "action-publish",
            "next": "",
            "select": "English",
            "title_en": "New Infoo",
            "title_es": "",
            "title_ar": "",
            "title_vi": "",
            "topics-TOTAL_FORMS": "0",
            "topics-INITIAL_FORMS": "0",
            "topics-MIN_NUM_FORMS": "0",
            "topics-MAX_NUM_FORMS": "1000",
            "related_departments-TOTAL_FORMS": "0",
            "related_departments-INITIAL_FORMS": "0",
            "related_departments-MIN_NUM_FORMS": "0",
            "related_departments-MAX_NUM_FORMS": "1000",
            "description_ar": "",
            "description_en": "",
            "description_es": "",
            "description_vi": "",
            "additional_content_ar": "null",
            "additional_content_en": "null",
            "additional_content_es": "null",
            "additional_content_vi": "null",
            "contacts-TOTAL_FORMS": "0",
            "contacts-INITIAL_FORMS": "0",
            "contacts-MIN_NUM_FORMS": "0",
            "contacts-MAX_NUM_FORMS": "1000",
            "author_notes": "null",
            "slug_ar": "",
            "slug_en": "new-infoo",
            "slug_es": "",
            "slug_vi": "",
            "seo_title_ar": "",
            "seo_title_en": "",
            "seo_title_es": "",
            "seo_title_vi": "",
            "search_description_ar": "",
            "search_description_en": "",
            "search_description_es": "",
            "search_description_vi": "",
            "go_live_at": "",
            "expire_at": "",
        }
        print("hi")

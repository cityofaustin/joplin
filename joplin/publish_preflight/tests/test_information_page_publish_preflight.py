import os
from django.test import TestCase

from .utils.make_form import make_form
from .utils.load_test_data import load_test_data

from pages.information_page.models import InformationPage
from pages.topic_page.models import TopicPage
from pages.topic_collection_page.models import TopicCollectionPage
from pages.department_page.models import DepartmentPage
import pytest

# pipenv run joplin/manage.py test publish_preflight.tests.test_information_page_publish_preflight

#
# class PublishPreflightInformationPage(TestCase):
#     # Load fresh data for every test to avoid cross-contamination
#     def setUp(self):
#         test_data = load_test_data()
#         for key in test_data:
#             setattr(self, key, test_data[key])
#
#     def test_setup_data_loaded(self):
#         self.assertTrue(isinstance(self.topic, TopicPage))
#         self.assertTrue(isinstance(self.topic_collection, TopicCollectionPage))
#         self.assertTrue(self.topic.topiccollections.count() == 1)
#         self.assertTrue(isinstance(self.department, DepartmentPage))
#         self.assertTrue(isinstance(self.info_page, InformationPage))
#
#     # Test that form is invalid if no publish requirements are added
#     # There should be 5 errors on the form (for missing additional_content, description, and a topic, related_department, or top_level)
#     def test_no_publish_required_fields(self):
#         fake_request = {
#             "action-publish": "action-publish",
#             "next": "",
#             "select": "English",
#             "title_en": "Adopt a baby tarantula",
#             "title_es": "",
#             "title_ar": "",
#             "title_vi": "",
#             "topics-TOTAL_FORMS": "0",
#             "topics-INITIAL_FORMS": "0",
#             "topics-MIN_NUM_FORMS": "0",
#             "topics-MAX_NUM_FORMS": "1000",
#             "related_departments-TOTAL_FORMS": "0",
#             "related_departments-INITIAL_FORMS": "0",
#             "related_departments-MIN_NUM_FORMS": "0",
#             "related_departments-MAX_NUM_FORMS": "1000",
#             "description_ar": "",
#             "description_en": "",
#             "description_es": "",
#             "description_vi": "",
#             "additional_content_ar": "null",
#             "additional_content_en": "null",
#             "additional_content_es": "null",
#             "additional_content_vi": "null",
#             "contacts-TOTAL_FORMS": "0",
#             "contacts-INITIAL_FORMS": "0",
#             "contacts-MIN_NUM_FORMS": "0",
#             "contacts-MAX_NUM_FORMS": "1000",
#             "author_notes": "null",
#             "slug_ar": "",
#             "slug_en": "new-infoo",
#             "slug_es": "",
#             "slug_vi": "",
#             "seo_title_ar": "",
#             "seo_title_en": "",
#             "seo_title_es": "",
#             "seo_title_vi": "",
#             "search_description_ar": "",
#             "search_description_en": "",
#             "search_description_es": "",
#             "search_description_vi": "",
#             "go_live_at": "",
#             "expire_at": "",
#         }
#         form = make_form(self.info_page, fake_request)
#         is_valid = form.is_valid()
#         self.assertFalse(is_valid)
#         self.assertEqual(form._errors["__all__"].data.__len__(), 5)
#
#     # Test that form is valid if:
#     # additional content, description, and a topic is selected
#     def test_all_publish_required_fields(self):
#         fake_request = {
#             "action-publish": "action-publish",
#             "next": "",
#             "select": "English",
#             "title_en": "Adopt a baby tarantula",
#             "title_es": "",
#             "title_ar": "",
#             "title_vi": "",
#             "topics-TOTAL_FORMS": "1",
#             "topics-INITIAL_FORMS": "0",
#             "topics-MIN_NUM_FORMS": "0",
#             "topics-MAX_NUM_FORMS": "1000",
#             "topics-0-topic": self.topic.pk,
#             "topics-0-id": "",
#             "topics-0-DELETE": "",
#             "related_departments-TOTAL_FORMS": "0",
#             "related_departments-INITIAL_FORMS": "0",
#             "related_departments-MIN_NUM_FORMS": "0",
#             "related_departments-MAX_NUM_FORMS": "1000",
#             "description_ar": "",
#             "description_en": "A Test Description.",
#             "description_es": "",
#             "description_vi": "",
#             "additional_content_ar": "null",
#             "additional_content_en": '{"blocks":[{"key":"fxwru","text":"Some test additional Content","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{}}',
#             "additional_content_es": "null",
#             "additional_content_vi": "null",
#             "contacts-TOTAL_FORMS": "0",
#             "contacts-INITIAL_FORMS": "0",
#             "contacts-MIN_NUM_FORMS": "0",
#             "contacts-MAX_NUM_FORMS": "1000",
#             "author_notes": "null",
#             "slug_ar": "",
#             "slug_en": "adopt-a-baby-tarantula",
#             "slug_es": "",
#             "slug_vi": "",
#             "seo_title_ar": "",
#             "seo_title_en": "",
#             "seo_title_es": "",
#             "seo_title_vi": "",
#             "search_description_ar": "",
#             "search_description_en": "",
#             "search_description_es": "",
#             "search_description_vi": "",
#             "go_live_at": "",
#             "expire_at": "",
#         }
#         form = make_form(self.info_page, fake_request)
#         is_valid = form.is_valid()
#         self.assertTrue(is_valid)
#
#     # A published page should not allow an update if the required topic_page field was removed
#     # There should be 3 errors on the form (for missing a topic, related_department, or top_level)
#     def test_removing_required_field(self):
#         information_page_topic = InformationPageTopic(**{
#             "page": self.info_page,
#             "topic": self.topic,
#         })
#         self.info_page.topics.add(information_page_topic)
#         self.info_page.save_revision()
#         self.info_page.get_latest_revision().publish()
#
#         fake_request = {
#             'action-publish': 'action-publish',
#             'next': '',
#             'select': 'English',
#             'title_en': 'Adopt a baby tarantula',
#             'title_es': '',
#             'title_ar': '',
#             'title_vi': '',
#             'topics-TOTAL_FORMS': '1',
#             'topics-INITIAL_FORMS': '1',
#             'topics-MIN_NUM_FORMS': '0',
#             'topics-MAX_NUM_FORMS': '1000',
#             'topics-0-topic': self.topic.pk,
#             'topics-0-id': '1',
#             'topics-0-DELETE': '1',
#             'related_departments-TOTAL_FORMS': '0',
#             'related_departments-INITIAL_FORMS': '0',
#             'related_departments-MIN_NUM_FORMS': '0',
#             'related_departments-MAX_NUM_FORMS': '1000',
#             'description_ar': '',
#             'description_en': 'A test description',
#             'description_es': '',
#             'description_vi': '',
#             'additional_content_ar': 'null',
#             'additional_content_en': '{"blocks":[{"key":"g1onp","text":"Look, additional content.","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{}}',
#             'additional_content_es': 'null',
#             'additional_content_vi': 'null',
#             'contacts-TOTAL_FORMS': '0',
#             'contacts-INITIAL_FORMS': '0',
#             'contacts-MIN_NUM_FORMS': '0',
#             'contacts-MAX_NUM_FORMS': '1000',
#             'author_notes': 'null',
#             'slug_ar': '',
#             'slug_en': 'adopt-a-baby-tarantula',
#             'slug_es': '',
#             'slug_vi': '',
#             'seo_title_ar': '',
#             'seo_title_en': '',
#             'seo_title_es': '',
#             'seo_title_vi': '',
#             'search_description_ar': '',
#             'search_description_en': '',
#             'search_description_es': '',
#             'search_description_vi': '',
#             'go_live_at': '',
#             'expire_at': '',
#         }
#         form = make_form(self.info_page, fake_request)
#         is_valid = form.is_valid()
#         self.assertFalse(is_valid)
#         self.assertEqual(form._errors["__all__"].data.__len__(), 3)

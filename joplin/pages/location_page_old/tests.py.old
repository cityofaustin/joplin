# from django.core.exceptions import ValidationError
# from django.test import TestCase
# from django.core.exceptions import NON_FIELD_ERRORS
# import pdb
# from pages.location_page.models import LocationPageRelatedServices
# from . import models, factories
# from contextlib import contextmanager
# import pytest
#
#
# @pytest.mark.xfail
# class LocationPageRelatedServiceTests(TestCase):
#     def setUp(self):
#         self.related_service = models.LocationPageRelatedServices()
#
#     def test_missing_related_service_hours_raises_error(self):
#         with self.assertRaisesMessage(Exception, 'Please either check this or input hours for this service'):
#             self.related_service.clean()
#
#     def test_missing_required_fields(self):
#         try:
#             self.related_service.full_clean()
#         except ValidationError as e:
#             self.assertTrue('hours_same_as_location' in e.message_dict)
#             self.assertTrue('related_service' in e.message_dict)
#             self.assertTrue('page' in e.message_dict)

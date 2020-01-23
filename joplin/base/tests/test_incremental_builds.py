from django.test import TestCase
from django.core.management import call_command
import os
from graphene import Node

from base.models import (
    TopicPage, TopicCollectionPage, ServicePage, GuidePage, InformationPage, OfficialDocumentPage, DepartmentPage,
    Map, Contact
)
from wagtail.documents.models import Document

from base.signals.janis_build_triggers import collect_pages, collect_pages_snippet


class TestCollectPages(TestCase):
    @classmethod
    def setUpTestData(cls):
        # setup test data: run once to set up non modified test data for all class methods
        # currently loading prod data. This is a short term solution since our prod data may be overwritten
        # and could disrupt the tests. Goal is to get some solid fixtures written that are tied to the tests
        print("loading test data: prod datadump...")
        os.environ['LOAD_DATA'] = 'prod'
        call_command('load_joplin_data')
        print("test data loaded")

    def test_official_document_page(self):
        changed_page = OfficialDocumentPage.objects.get(id=128)
        # returns our Official complaint and discipline documents page
        global_ids = collect_pages(changed_page)
        # Which is linked on the Office of Police Oversight Department Page
        department_page = DepartmentPage.objects.get(id=27)
        global_page_id = Node.to_global_id(department_page.get_verbose_name().lower(), department_page.id)
        self.assertTrue(global_page_id in global_ids)

    def test_service_page_in_guide_page(self):
        """
        Service Pages are inserted in Guide Pages in a ListBlock(PageChooserBlock) and are not connected by ForeignKeys
        """
        changed_page = ServicePage.objects.get(id=137)
        # Get food handler training and food manager certificates
        # is on <GuidePage: Mobile Food Permitting Process Guide>
        global_ids = collect_pages(changed_page)
        permit_guide = GuidePage.objects.get(id=172)
        global_page_id = Node.to_global_id(permit_guide.get_verbose_name().lower(), permit_guide.id)
        self.assertTrue(global_page_id in global_ids)

    def test_information_page_in_guide_page(self):
        '''
        Service Pages are inserted in Guide Pages in a ListBlock(PageChooserBlock) and are not connected by ForeignKeys
        '''
        changed_page = InformationPage.objects.get(id=121)
        # Mobile food vendor permit types and fees
        # is on <GuidePage: Mobile Food Permitting Process Guide>
        global_ids = collect_pages(changed_page)
        permit_guide = GuidePage.objects.get(id=172)
        global_page_id = Node.to_global_id(permit_guide.get_verbose_name().lower(), permit_guide.id)
        self.assertTrue(global_page_id in global_ids)

    def test_page_sibling_topic(self):
        """
        currently fails because topics don't know about sibling topics seen in the contextual nav
        :return:
        """
        changed_page = TopicPage.objects.get(id=58)
        # Compost and Food Waste topic page is listed as related to
        # Get your Bulk items collected
        bulk_items = ServicePage.objects.get(id=5)
        global_ids = collect_pages(changed_page)
        global_page_id = Node.to_global_id(bulk_items.get_verbose_name().lower(), bulk_items.id)
        self.assertTrue(global_page_id in global_ids)

    def test_topic_collection(self):
        # Topic Collection page: https://alpha.austin.gov/en/health-safety/health-records-certificates-2/
        changed_page = TopicCollectionPage.objects.get(id=50)
        # "health records and certificates" is seen on the Birth and Death Certificates contextual nav
        birth_cert = TopicPage.objects.get(id=51)
        global_ids = collect_pages(changed_page)
        global_page_id = Node.to_global_id(birth_cert.get_verbose_name().lower(), birth_cert.id)
        self.assertTrue(global_page_id in global_ids)

    def test_contact_update(self):
        changed_snippet = Contact.objects.get(id=10)
        # First Workers Day Labor Center
        global_ids = collect_pages_snippet(changed_snippet)
        find_work = ServicePage.objects.get(id=116)
        find_workers = ServicePage.objects.get(id=115)
        global_page_id1 = Node.to_global_id(find_work.get_verbose_name().lower(), find_work.id)
        global_page_id2 = Node.to_global_id(find_workers.get_verbose_name().lower(), find_workers.id)
        self.assertTrue(global_page_id1 in global_ids)
        self.assertTrue(global_page_id2 in global_ids)

    def test_map_update(self):
        """
        Not working. Maps are inserted in a Streamfield named dynamic content via
        SnippetChooserBlockWithAPIGoodness, no ForeignKey relationship
        """
        changed_snippet = Map.objects.get(id=1)
        global_ids = collect_pages_snippet(changed_snippet)
        pick_up_paint = ServicePage.objects.get(id=12)
        global_page_id = Node.to_global_id(pick_up_paint.get_verbose_name().lower(), pick_up_paint.id)
        self.assertTrue(global_page_id in global_ids)

    def test_document_update(self):
        changed_snippet = Document.objects.get(id=3)
        # One of the OPO documents
        global_ids = collect_pages_snippet(changed_snippet)
        page = OfficialDocumentPage.objects.get(id=128)
        # complaint and discipline documents page
        global_page_id = Node.to_global_id(page.get_verbose_name().lower(), page.id)
        self.assertTrue(global_page_id in global_ids)


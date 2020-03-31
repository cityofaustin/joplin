import pytest

from importer.page_importer import PageImporter
from pages.location_page.models import LocationPage
import pages.location_page.fixtures as fixtures
import pages.location_page.fixtures.helpers.components as components


@pytest.mark.django_db
def test_create_location_page_from_api(remote_staging_preview_url, remote_pytest_api):
    url = f'{remote_staging_preview_url}/location/UGFnZVJldmlzaW9uTm9kZToyMw==?CMS_API={remote_pytest_api}'
    page = PageImporter(url).fetch_page_data().create_page()
    assert isinstance(page, LocationPage)


@pytest.mark.django_db
def test_create_location_page_with_title():
    page = fixtures.title()
    assert isinstance(page, LocationPage)
    assert page.title == "Location page with title"
    assert page.slug == "location-page-with-title"




# # If location page is live
# # and coa_global=False (top level is not checked)
# @pytest.mark.django_db
# # def test_base_page_with_topics_with_department_not_global_urls():
# def test_location_page_with_urls():
#     # Using .create() here makes it so the factory also creates
#     # our GroupPagePermissions to associate departments
#     page = JanisBasePageWithTopicsFactory.create(
#         slug="location_page_slug",
#         coa_global=False,
#         add_location_page__dummy=True,
#     )
#
#     # Set expected urls using departments and topic pages
#     expected_urls = []
#     # expected_urls.extend(['http://fake.base.url/{department_slug}/{page_slug}/'.format(
#     #     department_slug=permission.group.department.department_page.slug, page_slug=page.slug) for permission in
#     #                       page.group_permissions.all()])
#
#     expected_urls.extend(['{base_url}{page_type}/{page_slug}'.format(base_url=self.janis_url_base('publish_janis_branch'),
#                                                            page_type=self.janis_url_page_type, page_slug=self.slug)]
#
#     # for base_page_topic in page.topics.all():
#     #     expected_urls.extend(
#     #         ['{topic_url}page_slug/'.format(topic_url=url) for url in base_page_topic.topic.janis_urls()])
#
#     urls = page.janis_urls()
#     url = page.janis_url()
#
#     # we should get a url under every department
#     assert urls == expected_urls
#     assert url == expected_urls[0]

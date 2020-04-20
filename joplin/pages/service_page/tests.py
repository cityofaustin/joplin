import pytest

from importer.page_importer import PageImporter
from pages.service_page.models import ServicePage
import pages.service_page.fixtures as fixtures
import pages.service_page.fixtures.helpers.components as components
import pages.location_page.fixtures as location_page_fixtures
import pages.topic_page.fixtures as topic_page_fixtures


@pytest.mark.django_db
def test_create_service_page_from_api(remote_staging_preview_url, test_api_url, test_api_jwt_token):
    url = f'{remote_staging_preview_url}/services/UGFnZVJldmlzaW9uTm9kZToxNQ==?CMS_API={test_api_url}'
    page = PageImporter(url, test_api_jwt_token).fetch_page_data().create_page()
    assert isinstance(page, ServicePage)


@pytest.mark.django_db
def test_create_service_page_with_contact_from_api(remote_staging_preview_url, test_api_url, test_api_jwt_token):
    url = f'{remote_staging_preview_url}/services/UGFnZVJldmlzaW9uTm9kZToyMA==?CMS_API={test_api_url}'
    page = PageImporter(url, test_api_jwt_token).fetch_page_data().create_page()
    assert isinstance(page, ServicePage)
    assert page.title == 'Service page with contact'
    assert page.contact.name == 'Contact name'


@pytest.mark.django_db
def test_create_service_page_with_department_from_api(remote_staging_preview_url, test_api_url, test_api_jwt_token):
    url = f'{remote_staging_preview_url}/services/UGFnZVJldmlzaW9uTm9kZTozNg==?CMS_API={test_api_url}'
    page = PageImporter(url, test_api_jwt_token).fetch_page_data().create_page()
    assert isinstance(page, ServicePage)
    assert page.title == 'Service page with department'
    group_page_permission = page.group_permissions.all()[0]
    assert group_page_permission.group.name == 'Pytest department'
    assert group_page_permission.group.department.department_page.slug == 'pytest-department'
    assert group_page_permission.page == page


@pytest.mark.django_db
def test_create_service_page_with_one_imported_and_some_unimported_internal_links_from_api(remote_staging_preview_url, test_api_url, test_api_jwt_token):
    # this fixture has the same slug as the first link of the page we're importing,
    # let's create it so the importer can link to it
    topic_page_fixtures.title()

    expected_steps = components.step_with_one_imported_and_some_unimported_internal_links()
    url = f'{remote_staging_preview_url}/services/UGFnZVJldmlzaW9uTm9kZTo1MQ==?CMS_API={test_api_url}'
    page = PageImporter(url, test_api_jwt_token).fetch_page_data().create_page()
    assert isinstance(page, ServicePage)
    for i, step in enumerate(page.steps.stream_data):
        assert step["type"] == expected_steps[i]["type"]
        assert step["value"] == expected_steps[i]["value"]
    # since some of the imported links are using placeholder pages, we shouldn't be live yet
    assert not page.live


@pytest.mark.django_db
def test_create_service_page_with_title():
    page = fixtures.title()
    assert isinstance(page, ServicePage)
    assert page.title == "Service Page with title"
    assert page.slug == "service-page-with-title"


@pytest.mark.django_db
def test_create_service_page_with_2_steps():
    page = fixtures.steps_2()
    expected_steps = components.steps_2
    assert isinstance(page, ServicePage)
    assert page.title == "Service Page with 2 Steps"
    assert page.slug == "2-step-yee-haw"
    for i, step in enumerate(page.steps.stream_data):
        assert step["type"] == expected_steps[i]["type"]
        assert step["value"] == expected_steps[i]["value"]


@pytest.mark.django_db
def test_create_service_page_with_appblock_steps():
    page = fixtures.steps_with_appblocks()
    expected_steps = components.steps_with_appblocks
    assert isinstance(page, ServicePage)
    assert page.title == "Service Page with Appblock steps"
    assert page.slug == "service-page-appblocks"
    for i, step in enumerate(page.steps.stream_data):
        assert step["type"] == expected_steps[i]["type"]
        assert step["value"] == expected_steps[i]["value"]


@pytest.mark.django_db
def test_create_service_page_with_step_with_options():
    page = fixtures.step_with_options()
    expected_steps = components.step_with_options

    assert isinstance(page, ServicePage)
    assert page.title == "Service Page with a Step with options"
    assert page.slug == "step-with-yee-or-haw"
    for i, step in enumerate(page.steps.stream_data):
        assert step["type"] == expected_steps[i]["type"]
        assert step["value"] == expected_steps[i]["value"]


@pytest.mark.django_db
def test_create_service_page_with_new_contact():
    page = fixtures.new_contact()
    assert isinstance(page, ServicePage)

    assert page.title == 'Service page with new contact'
    assert page.contact.name == 'New contact'


@pytest.mark.django_db
def test_create_service_page_with_dynamic_content_list():
    page = fixtures.dynamic_content_list()
    expected_dynamic_content_blocks = components.dynamic_content_list

    assert isinstance(page, ServicePage)
    # todo: figure out what we want this to assert
    assert page.title == 'Service Page with dynamic content list'
    for i, dynamic_content_block in enumerate(page.dynamic_content.stream_data):
        assert dynamic_content_block["type"] == expected_dynamic_content_blocks[i]["type"]

        # somewhere in the json of it all this happens, it doesn't seem to be an issue for wagtail
        # so for now let's just account for it in this test
        if dynamic_content_block["value"] == 'None':
            dynamic_content_block["value"] = None

        assert dynamic_content_block["value"] == expected_dynamic_content_blocks[i]["value"]


@pytest.mark.django_db
def test_kitchen_sink():
    page = fixtures.kitchen_sink()
    assert isinstance(page, ServicePage)


@pytest.mark.django_db
def test_create_service_page_with_step_with_1_location():
    page = fixtures.step_with_1_location()
    expected_steps = components.step_with_1_location()

    assert isinstance(page, ServicePage)
    assert page.title == "Service Page with 1 location step"
    assert page.slug == "service-page-with-1-location-step"
    for i, step in enumerate(page.steps.stream_data):
        assert step["type"] == expected_steps[i]["type"]
        assert step["value"] == expected_steps[i]["value"]


@pytest.mark.django_db
def test_create_service_page_with_step_with_2_locations():
    page = fixtures.step_with_2_locations()
    expected_steps = components.step_with_2_locations()

    assert isinstance(page, ServicePage)
    assert page.title == "Service Page with 2 locations step"
    assert page.slug == "service-page-with-2-locations-step"
    for i, step in enumerate(page.steps.stream_data):
        assert step["type"] == expected_steps[i]["type"]
        assert step["value"] == expected_steps[i]["value"]


@pytest.mark.django_db
def test_import_step_with_1_already_existing_location(remote_staging_preview_url, test_api_url, test_api_jwt_token):
    location_page = location_page_fixtures.title()
    url = f'{remote_staging_preview_url}/services/UGFnZVJldmlzaW9uTm9kZTo1OA==?CMS_API={test_api_url}'
    page = PageImporter(url, test_api_jwt_token).fetch_page_data().create_page()
    assert isinstance(page, ServicePage)
    assert page.live
    # The importer should assign the step's location to our matching location_page.
    assert page.steps.stream_data[0]["value"]["locations"][0] == location_page.pk


@pytest.mark.django_db
def test_import_step_with_1_new_location(remote_staging_preview_url, test_api_url, test_api_jwt_token):
    url = f'{remote_staging_preview_url}/services/UGFnZVJldmlzaW9uTm9kZTo1OA==?CMS_API={test_api_url}'
    page = PageImporter(url, test_api_jwt_token).fetch_page_data().create_page()
    assert isinstance(page, ServicePage)
    assert not page.live
    # The importer should delete the location because it hasn't been imported yet.
    # TODO: update API to allow creation of location_page from step data
    assert not page.steps


@pytest.mark.django_db
def test_import_step_with_1_already_existing_location_1_new_location(remote_staging_preview_url, test_api_url, test_api_jwt_token):
    location_page = location_page_fixtures.title()
    url = f'{remote_staging_preview_url}/services/UGFnZVJldmlzaW9uTm9kZTo2Mg==?CMS_API={test_api_url}'
    page = PageImporter(url, test_api_jwt_token).fetch_page_data().create_page()
    assert isinstance(page, ServicePage)
    assert not page.live
    assert len(page.steps.stream_data[0]["value"]["locations"]) == 1
    assert page.steps.stream_data[0]["value"]["locations"][0] == location_page.pk


@pytest.mark.django_db
def test_import_step_with_2_already_existing_locations(remote_staging_preview_url, test_api_url, test_api_jwt_token):
    location_page_1 = location_page_fixtures.title()
    location_page_2 = location_page_fixtures.live_library()
    url = f'{remote_staging_preview_url}/services/UGFnZVJldmlzaW9uTm9kZTo2Mg==?CMS_API={test_api_url}'
    page = PageImporter(url, test_api_jwt_token).fetch_page_data().create_page()
    assert isinstance(page, ServicePage)
    assert page.live
    assert page.steps.stream_data[0]["value"]["locations"][0] == location_page_1.pk
    assert page.steps.stream_data[0]["value"]["locations"][1] == location_page_2.pk

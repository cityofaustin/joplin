import pytest

from importer.page_importer import PageImporter
from pages.service_page.models import ServicePage
import pages.service_page.fixtures as fixtures
import pages.service_page.fixtures.helpers.components as components


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
def test_kitchen_sink():
    page = fixtures.kitchen_sink()
    assert isinstance(page, ServicePage)

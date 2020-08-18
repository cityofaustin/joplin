from pages.department_page.factories import DepartmentPageFactory
from pages.department_page.models import DepartmentPage
from importer.page_importer import PageImporter
from groups.factories import DepartmentFactory
import pytest


# If we don't have any associated department group
@pytest.mark.django_db
def test_department_page_no_department_group(home_page):
    page = DepartmentPageFactory.create(slug="department_slug", parent=home_page)

    urls = page.janis_urls()
    janis_publish_url = page.janis_publish_url()

    assert urls == []
    assert janis_publish_url == '#'


# If we don't have any associated department group
@pytest.mark.django_db
def test_department_page_with_department_group(home_page, expected_publish_url_base):
    department = DepartmentFactory.create(add_department_page__dummy=True, add_department_page__parent=home_page)
    page = department.department_page

    urls = page.janis_urls()
    janis_publish_url = page.janis_publish_url()

    assert urls == [f'/{page.slug}/']
    assert janis_publish_url == f'{expected_publish_url_base}/{page.slug}/'


@pytest.mark.django_db
def test_create_department_page_from_api(remote_staging_preview_url, test_api_url, test_api_jwt_token):
    url = f'{remote_staging_preview_url}/department/UGFnZVJldmlzaW9uTm9kZToyNg==?CMS_API={test_api_url}'
    page = PageImporter(url, test_api_jwt_token).fetch_page_data().create_page()
    assert isinstance(page, DepartmentPage)

from pages.department_page.factories import DepartmentPageFactory
from groups.factories import DepartmentFactory
import pytest


# If we don't have any associated department group
@pytest.mark.django_db
def test_department_page_no_department_group():
    page = DepartmentPageFactory.build(slug="department_slug")

    urls = page.janis_urls()
    url = page.janis_url()

    assert urls == []
    assert url == '#'


# If we don't have any associated department group
@pytest.mark.django_db
def test_department_page_with_department_group():
    department = DepartmentFactory.create(add_department_page__dummy=True)
    page = department.department_page

    urls = page.janis_urls()
    url = page.janis_url()

    assert urls == ['http://fake.base.url/{department_slug}/'.format(department_slug=page.slug)]
    assert url == 'http://fake.base.url/{department_slug}/'.format(department_slug=page.slug)

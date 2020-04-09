from pages.department_page.factories import DepartmentPageFactory
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
    department = DepartmentFactory.create(add_department_page__dummy=True)
    page = department.department_page

    # Adds an already saved page to a new homepage.
    # home_page.add_child(instance=page) will not work since "page" has already been saved to the database.
    page.move(home_page, 'last-child')
    # Refreshing allows the "page" object to know that its parent is now "home_page".
    # We need page.get_parent() to work in order to get page.janis_publish_url()
    page.refresh_from_db()

    urls = page.janis_urls()
    janis_publish_url = page.janis_publish_url()

    assert urls == [f'/{page.slug}/']
    assert janis_publish_url == f'{expected_publish_url_base}/{page.slug}/'

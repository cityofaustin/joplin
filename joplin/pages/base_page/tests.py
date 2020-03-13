from pages.base_page.factories import JanisBasePageFactory
import pytest


# If we don't have any associated department,
# and coa_global=False (top level page isn't checked)
@pytest.mark.django_db
def test_base_page_no_department_not_global_urls():
    page = JanisBasePageFactory.build(slug="global_slug", coa_global=False)
    urls = page.janis_urls()
    assert urls == []


@pytest.mark.django_db
def test_base_page_no_department_not_global_url():
    page = JanisBasePageFactory.build(slug="global_slug", coa_global=False)
    url = page.janis_url()
    assert url == '#'

# If we don't have any associated department,
# and coa_global=True (top level is checked)
@pytest.mark.django_db
def test_base_page_no_department_coa_global_urls():
    page = JanisBasePageFactory.build(slug="global_slug", coa_global=True)
    urls = page.janis_urls()

    # since it's global, it should ignore the departments and just publish at the top level
    assert urls == ['http://fake.base.url/global_slug/']

@pytest.mark.django_db
def test_base_page_no_department_coa_global_url():
    page = JanisBasePageFactory.build(slug="global_slug", coa_global=True)
    url = page.janis_url()
    assert url == 'http://fake.base.url/global_slug/'


# If we have an associated department,
# and coa_global=True (top level is checked)
@pytest.mark.django_db
def test_base_page_with_department_coa_global_urls():
    page = JanisBasePageFactory.build(slug="global_slug", coa_global=True)
    # todo associate department here
    urls = page.janis_urls()

    # since it's global, it should ignore the departments and just publish at the top level
    assert urls == ['http://fake.base.url/global_slug/']


@pytest.mark.django_db
def test_base_page_with_department_coa_global_url():
    page = JanisBasePageFactory.build(slug="global_slug", coa_global=True)
    # todo associate department here
    url = page.janis_url()
    assert url == 'http://fake.base.url/global_slug/'

# If we have an associated department,
# and coa_global=False (top level is not checked)
@pytest.mark.django_db
def test_base_page_with_department_not_global_urls():
    page = JanisBasePageFactory.create(slug="global_slug", coa_global=False)
    # todo associate department here
    urls = page.janis_urls()

    # since it's global, it should ignore the departments and just publish at the top level
    assert urls == ['http://fake.base.url/global_slug/']


@pytest.mark.django_db
def test_base_page_with_department_not_global_url():
    page = JanisBasePageFactory.create(slug="global_slug", coa_global=False)
    # todo associate department here
    url = page.janis_url()
    assert url == 'http://fake.base.url/global_slug/'

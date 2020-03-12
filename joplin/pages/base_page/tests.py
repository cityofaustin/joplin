from pages.base_page.factories import JanisBasePageFactory
import pytest


@pytest.mark.django_db
def test_base_page_coa_global_url():
    page = JanisBasePageFactory.build(slug="global_slug", coa_global=True)
    url = page.janis_url()
    assert url == 'http://fake.base.url/global_slug/'


@pytest.mark.django_db
def test_base_page_no_url():
    page = JanisBasePageFactory.build(slug="global_slug", coa_global=False)
    url = page.janis_url()
    assert url == '#'

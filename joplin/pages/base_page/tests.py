from pages.base_page.factories import JanisBasePageFactory, JanisBasePageWithTopicsFactory
import pytest


# If we don't have any associated department,
# and coa_global=False (top level page isn't checked)
@pytest.mark.django_db
def test_base_page_no_department_not_global_urls():
    page = JanisBasePageFactory.build(slug="global_slug", coa_global=False)

    urls = page.janis_urls()
    url = page.janis_url()

    assert urls == []
    assert url == '#'


# If we don't have any associated department,
# and coa_global=True (top level is checked)
@pytest.mark.django_db
def test_base_page_no_department_coa_global_urls():
    page = JanisBasePageFactory.build(slug="global_slug", coa_global=True)
    urls = page.janis_urls()
    url = page.janis_url()

    # since it's global, it should ignore the departments and just publish at the top level
    assert urls == ['http://fake.base.url/global_slug/']
    assert url == 'http://fake.base.url/global_slug/'


# If we have an associated department,
# and coa_global=True (top level is checked)
@pytest.mark.django_db
def test_base_page_with_department_coa_global_urls():
    page = JanisBasePageFactory.build(slug="global_slug", coa_global=True)
    urls = page.janis_urls()
    url = page.janis_url()

    # since it's global, it should ignore the departments and just publish at the top level
    assert urls == ['http://fake.base.url/global_slug/']
    assert url == 'http://fake.base.url/global_slug/'


# If we have an associated department,
# and coa_global=False (top level is not checked)
@pytest.mark.django_db
def test_base_page_with_department_not_global_urls():
    # Using .create() here makes it so the factory also creates
    # our GroupPagePermissions to associate departments
    page = JanisBasePageFactory.create(slug="page_slug", coa_global=False)

    # Set expected urls using group page permission department slugs
    expected_urls = ['http://fake.base.url/{department_slug}/{page_slug}/'.format(
        department_slug=permission.group.department.department_page.slug, page_slug=page.slug) for permission in
                     page.group_permissions.all()]

    urls = page.janis_urls()
    url = page.janis_url()

    # we should get a url under every department
    assert urls == expected_urls
    assert url == expected_urls[0]


# If we don't have any associated department,
# and we don't have any associated topic pages
# and coa_global=False (top level page isn't checked)
@pytest.mark.django_db
def test_base_page_with_topics_no_topic_no_department_not_global_urls():
    page = JanisBasePageWithTopicsFactory.build(slug="global_slug", coa_global=False)

    urls = page.janis_urls()
    url = page.janis_url()

    assert urls == []
    assert url == '#'


# If we don't have any associated department,
# and we don't have any associated topic pages
# and coa_global=True (top level page is checked)
@pytest.mark.django_db
def test_base_page_with_topics_no_topic_no_department_not_global_urls():
    page = JanisBasePageWithTopicsFactory.build(slug="global_slug", coa_global=True)

    urls = page.janis_urls()
    url = page.janis_url()

    assert urls == ['http://fake.base.url/global_slug/']
    assert url == 'http://fake.base.url/global_slug/'

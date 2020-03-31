from pages.base_page.factories import JanisBasePageFactory
from pages.topic_page.factories import JanisBasePageWithTopicsFactory
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
    page = JanisBasePageFactory.create(
        slug="page_slug",
        coa_global=False,
        add_department__dummy=True,
    )

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


# # If we don't have any associated department,
# # and we don't have any associated topic pages
# # and coa_global=True (top level page is checked)
@pytest.mark.django_db
def test_base_page_with_topics_no_topic_no_department_coa_global_urls():
    page = JanisBasePageWithTopicsFactory.build(slug="global_slug", coa_global=True)

    urls = page.janis_urls()
    url = page.janis_url()

    assert urls == ['http://fake.base.url/global_slug/']
    assert url == 'http://fake.base.url/global_slug/'


# If we have associated departments,
# and we have associated topic pages
# and coa_global=False (top level is not checked)
@pytest.mark.django_db
def test_base_page_with_topics_with_department_not_global_urls():
    # Using .create() here makes it so the factory also creates
    # our GroupPagePermissions to associate departments
    page = JanisBasePageWithTopicsFactory.create(
        slug="page_slug",
        coa_global=False,
        add_topics__dummy=True
    )

    # Set expected urls using departments and topic pages
    expected_urls = []
    expected_urls.extend(['http://fake.base.url/{department_slug}/{page_slug}/'.format(
        department_slug=permission.group.department.department_page.slug, page_slug=page.slug) for permission in
                          page.group_permissions.all()])

    for base_page_topic in page.topics.all():
        expected_urls.extend(
            ['{topic_url}page_slug/'.format(topic_url=url) for url in base_page_topic.topic.janis_urls()])

    urls = page.janis_urls()
    url = page.janis_url()

    # we should get a url under every department
    assert urls == expected_urls
    assert url == expected_urls[0]


# todo: figure out how to get department permissions working in a test db setting so we don't get random failures
# If we have associated departments,
# and we have associated topic pages
# and coa_global=True (top level is checked)
# @pytest.mark.django_db
# def test_base_page_with_topics_with_topic_with_department_coa_global_urls():
#     page = JanisBasePageWithTopicsFactory.create(slug="global_slug_2", coa_global=True)
#
#     urls = page.janis_urls()
#     url = page.janis_url()
#
#     assert urls == ['http://fake.base.url/global_slug_2/']
#     assert url == 'http://fake.base.url/global_slug_2/'

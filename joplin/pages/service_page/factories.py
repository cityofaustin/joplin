import factory
import json
import wagtail_factories
from django.utils.text import slugify
from pages.topic_page.models import TopicPage
from pages.service_page.models import ServicePage, ServicePageContact
from pages.factory import PageFactory
from base.models import Contact
from pytest_factoryboy import register
from wagtail.core.models import Page
from pages.topic_page.factories import JanisBasePageWithTopicsFactory, create_topic_page_from_page_dictionary
from pages.home_page.models import HomePage


class ServicePageFactory(JanisBasePageWithTopicsFactory):
    class Meta:
        model = ServicePage


def create_service_page_from_page_dictionary(page_dictionary, revision_id):
    # Check if page with revision_id has already been imported
    try:
        page = ServicePage.objects.get(imported_revision_id=revision_id)
    except ServicePage.DoesNotExist:
        page = None
    if page:
        return page

    # Check if page with slug has already been imported
    try:
        page = ServicePage.objects.get(slug=page_dictionary['slug'])
    except ServicePage.DoesNotExist:
        page = None
    if page:
        return page

    # since we don't have a page matching the revision id or the slug
    # we need to create a page, which needs a topic if it has one
    # run through the topic logic here
    topic_page_dictionaries = [edge['node']['topic'] for edge in page_dictionary['topics']['edges']]
    topic_pages = [create_topic_page_from_page_dictionary(dictionary, dictionary['liveRevision']['id']) for dictionary
                   in topic_page_dictionaries]

    # todo: actually get departments here
    related_departments = ['just a string']

    # Set home as parent
    # todo: move this to base page factory?
    home = HomePage.objects.first()

    steps = json.dumps([
        {
            u'type': u'{0}'.format(step['type']),
            u'value': u'{0}'.format(step['value'])
        }
        for step in page_dictionary['steps']
    ])

    page = ServicePageFactory.create(
        imported_revision_id=revision_id,
        title=page_dictionary['title'],
        slug=page_dictionary['slug'],
        add_topics={'topics': topic_pages},
        add_related_departments=related_departments,
        coa_global=page_dictionary['coaGlobal'],
        parent=home,
        steps=steps,
        dynamic_content=page_dictionary['dynamicContent'],
        additional_content=page_dictionary['additionalContent'],
        short_description=page_dictionary['shortDescription'],
    )

    return page

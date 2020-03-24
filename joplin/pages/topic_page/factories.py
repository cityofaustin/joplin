import factory
from pages.topic_page.models import TopicPage, JanisBasePageTopic, JanisBasePageWithTopics
from pages.topic_collection_page.factories import JanisBasePageWithTopicCollectionsFactory, \
    create_topic_collection_page_from_importer_dictionaries
from pages.home_page.models import HomePage
from wagtail.core.models import Page

from pages.base_page.factories import JanisBasePageFactory


class TopicPageFactory(JanisBasePageWithTopicCollectionsFactory):
    class Meta:
        model = TopicPage


class JanisBasePageTopicFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base_page.factories.JanisBasePageWithTopicsFactory')
    topic = factory.SubFactory(TopicPageFactory)

    class Meta:
        model = JanisBasePageTopic


class JanisBasePageWithTopicsFactory(JanisBasePageFactory):
    class Meta:
        model = JanisBasePageWithTopics

    @factory.post_generation
    def add_topics(self, create, extracted, **kwargs):
        if extracted:
            # A list of topics were passed in, use them
            for topic in extracted['topics']:
                # todo: check to see if we already have the basepagetopiccollection objects made
                JanisBasePageTopicFactory.create(page=self, topic=topic)
            return

        # todo figure out if this is really what we want this factory to do
        if create:
            JanisBasePageTopicFactory.create_batch(2, page=self)


def create_topic_page_from_page_dictionary(page_dictionary, revision_id):
    # first check to see if we already imported this page
    # if we did, just go to the edit page for it without changing the db
    # todo: maybe change this to allow updating pages in the future?
    try:
        page = TopicPage.objects.get(imported_revision_id=revision_id)
    except TopicPage.DoesNotExist:
        page = None
    if page:
        return page

    # since we don't have a page matching the revision id, we should look
    # for other matches, for now let's just use slug
    # todo: figure out what we want the logic around importing a page with the same slug to look like
    try:
        page = TopicPage.objects.get(slug=page_dictionary['slug'])
    except TopicPage.DoesNotExist:
        page = None
    if page:
        return page

    # since we don't have a page matching the revision id or the slug
    # we need to create a page, which needs a topic collection if it has one
    # run through the topic collection logic here
    topic_collection_page_dictionaries = [edge['node']['topiccollection'] for edge in
                                          page_dictionary['topiccollections']['edges']]

    topic_collection_pages = [
        create_topic_collection_page_from_page_dictionary(dictionary, dictionary['liveRevision']['id']) for dictionary
        in topic_collection_page_dictionaries]

    # todo: actually get departments here
    related_departments = ['just a string']

    # Set home as parent
    # todo: move this to base page factory?
    home = HomePage.objects.first()

    # make the page
    page = TopicPageFactory.create(imported_revision_id=revision_id, title=page_dictionary['title'],
                                   slug=page_dictionary['slug'], description=page_dictionary['description'],
                                   add_topic_collections=topic_collection_pages,
                                   add_related_departments=related_departments, parent=home)

    return page

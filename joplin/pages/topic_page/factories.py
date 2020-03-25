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
        # TODO: add option to pass in already created topics
        if extracted:
            # A list of topics were passed in, use them
            for topic in extracted['topics']:
                # todo: check to see if we already have the basepagetopiccollection objects made
                JanisBasePageTopicFactory.create(page=self, topic=topic)
            return

        # pass "add_topics__dummy"=True into Factory() to make dummy topics
        if create:
            if (kwargs.get("dummy", False)):
                JanisBasePageTopicFactory.create_batch(2, page=self)


def create_topic_page_from_importer_dictionaries(page_dictionaries, revision_id):
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
    # for other matches, for now let's just use the english slug
    # todo: figure out what we want the logic around importing a page with the same slug to look like
    try:
        page = TopicPage.objects.get(slug=page_dictionaries['en']['slug'])
    except TopicPage.DoesNotExist:
        page = None
    if page:
        return page

    # since we don't have a page matching the revision id or the slug
    # make the combined page dictionary
    combined_dictionary = page_dictionaries['en']

    # associate/create topic collection pages
    topic_collection_pages = []
    for index in range(len(page_dictionaries['en']['topiccollections']['edges'])):
        topic_collection_pages.append(create_topic_collection_page_from_importer_dictionaries({
            'en': page_dictionaries['en']['topiccollections']['edges'][index]['node']['topiccollection'],
            'es': page_dictionaries['es']['topiccollections']['edges'][index]['node']['topiccollection'],
        }, page_dictionaries['en']['topiccollections']['edges'][index]['node']['topiccollection']['live_revision']['id']))
    combined_dictionary['add_topic_collections'] = topic_collection_pages

    # remove topiccollections if we have it because:
    # * it's in english only
    # * the factory doesn't know what to do with it
    # todo: why isn't pop working?
    if 'topiccollections' in combined_dictionary:
        del combined_dictionary['topiccollections']

    # remove liveRevision if we have it
    # todo: why isn't pop working?
    if 'live_revision' in combined_dictionary:
        del combined_dictionary['live_revision']

    # set the revision id
    combined_dictionary['imported_revision_id'] = revision_id

    # Set home as parent
    combined_dictionary['parent'] = HomePage.objects.first()

    # set the translated fields
    for field in TopicPageFactory._meta.model._meta.fields:
        if field.column.endswith("_es"):
            if field.column[:-3] in page_dictionaries['es']:
                combined_dictionary[field.column] = page_dictionaries['es'][field.column[:-3]]

    # todo: actually get departments here
    combined_dictionary['add_related_departments'] = ['just a string']

    page = TopicPageFactory.create(**combined_dictionary)
    return page

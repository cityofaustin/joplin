from pages.topic_page.models import TopicPage
from pages.topic_collection_page.factories import JanisBasePageWithTopicCollectionsFactory, \
    create_topic_collection_page_from_page_dictionary
from wagtail.core.models import Page


class TopicPageFactory(JanisBasePageWithTopicCollectionsFactory):
    class Meta:
        model = TopicPage


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

    # Set home as parent
    # todo: not hardcode home
    # todo: move this to base page factory?
    home = Page.objects.get(id=2)

    # make the page
    page = TopicPageFactory.create(imported_revision_id=revision_id, title=page_dictionary['title'],
                                   slug=page_dictionary['slug'], description=page_dictionary['description'],
                                   add_topic_collections=topic_collection_pages, parent=home)

    return page

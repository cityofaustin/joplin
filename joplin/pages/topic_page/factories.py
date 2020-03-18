from pages.topic_page.models import TopicPage
from pages.topic_collection_page.factories import JanisBasePageWithTopicCollectionsFactory


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
    topic_collection_page_revision_ids = []
    # todo get topic collection page revision ids in and then use importer to make the pages
    topic_collection_pages = []



    # todo: use something other than slug here
    # todo: add imported id to themes
    try:
        theme = Theme.objects.get(slug=page_dictionary['theme']['slug'])
    except Theme.DoesNotExist:
        theme = None
    if not theme:
        theme = ThemeFactory.create(slug=page_dictionary['theme']['slug'],
                                    text=page_dictionary['theme']['text'],
                                    description=page_dictionary['theme']['description'])

    # Set home as parent
    # todo: not hardcode home
    # todo: move this to base page factory?
    home = Page.objects.get(id=2)

    # make the page
    page = TopicCollectionPageFactory.create(imported_revision_id=revision_id, title=page_dictionary['title'],
                                             slug=page_dictionary['slug'], description=page_dictionary['description'],
                                             theme=theme, parent=home)

    return page

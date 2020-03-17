import factory
from pages.topic_collection_page.models import TopicCollectionPage, JanisBasePageTopicCollection, JanisBasePageWithTopicCollections
from pages.base_page.factories import JanisBasePageFactory
from pages.factory import PageFactory
from base.models import Theme
from wagtail.core.models import Page


class ThemeFactory(factory.django.DjangoModelFactory):
    slug = 'theme_slug'

    class Meta:
        model = Theme


class TopicCollectionPageFactory(PageFactory):
    theme = factory.SubFactory(ThemeFactory)

    class Meta:
        model = TopicCollectionPage


class JanisBasePageTopicCollectionFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base_page.factories.JanisBasePageWithTopicCollectionsFactory')
    topic_collection = factory.SubFactory(TopicCollectionPageFactory)

    class Meta:
        model = JanisBasePageTopicCollection


class JanisBasePageWithTopicCollectionsFactory(JanisBasePageFactory):
    class Meta:
        model = JanisBasePageWithTopicCollections

    @factory.post_generation
    def create_related_objects(self, create, extracted, **kwargs):
        if create:
            JanisBasePageTopicCollectionFactory.create_batch(2, page=self)

def create_topic_collection_page_from_page_dictionary(page_dictionary, revision_id):
    # first check to see if we already imported this page
    # if we did, just go to the edit page for it without changing the db
    # todo: maybe change this to allow updating pages in the future?
    page = TopicCollectionPage.objects.get(imported_revision_id=revision_id)
    if page:
        return page.id

    # since we don't have a page matching the revision id, we should look
    # for other matches, for now let's just use slug
    # todo: figure out what we want the logic around importing a page with the same slug to look like
    page = TopicCollectionPage.objects.get(slug=page_dictionary['slug'])
    if page:
        return page.id

    # since we don't have a page matching the revision id or the slug
    # we need to create a page, first we need to
    # check to see if we already have this theme imported
    # todo: use something other than slug here
    # todo: add imported id to themes
    theme = Theme.objects.get(slug=page_dictionary['theme']['slug'])
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

    return page.id

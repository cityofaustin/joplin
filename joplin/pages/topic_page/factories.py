from pages.topic_page.models import TopicPage
from pages.topic_collection_page.factories import JanisBasePageWithTopicCollectionsFactory


class TopicPageFactory(JanisBasePageWithTopicCollectionsFactory):

    class Meta:
        model = TopicPage

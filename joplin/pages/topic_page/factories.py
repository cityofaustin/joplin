from pages.topic_page.models import TopicPage
from pages.factory import PageFactory


class TopicPageFactory(PageFactory):

    class Meta:
        model = TopicPage

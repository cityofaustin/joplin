from pages.news_page.models import NewsPage
from pages.topic_page.factories import JanisBasePageFactory


class NewsPageFactory(JanisBasePageFactory):
    class Meta:
        model = NewsPage

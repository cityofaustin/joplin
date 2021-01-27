from pages.guide_page.models import GuidePage
from pages.topic_page.factories import JanisBasePageWithTopicsFactory


class GuidePageFactory(JanisBasePageWithTopicsFactory):
    class Meta:
        model = GuidePage

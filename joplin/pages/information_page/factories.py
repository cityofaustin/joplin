from pages.information_page.models import InformationPage
from pages.topic_page.factories import JanisBasePageWithTopicsFactory

class InformationPageFactory(JanisBasePageWithTopicsFactory):
    class Meta:
        model = InformationPage

import factory
import wagtail_factories
from base.models import HomePage
from pages.factory import PageFactory


class HomePageFactory(PageFactory):

    class Meta:
        model = HomePage

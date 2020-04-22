from pages.home_page.models import HomePage
from pages.factory import PageFactory


class HomePageFactory(PageFactory):
    class Meta:
        model = HomePage

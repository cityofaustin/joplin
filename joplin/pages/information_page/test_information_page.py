from pages.information_page.models import InformationPageContact
from pages.information_page.factory import InformationPageContactFactory, InformationPageFactory
import pytest


@pytest.mark.django_db
def test_information_page_factory(information_page_factory):
    page = information_page_factory.build(description="Dark and stormy")
    assert page.description == "Dark and stormy"

from pages.information_page.models import InformationPageContact
from pages.information_page.factories import InformationPageContactFactory, InformationPageFactory
import pytest


@pytest.mark.django_db
def test_information_page_factory(information_page_factory):
    page = InformationPageFactory.build(description="Dark and stormy")
    assert page.description == "Dark and stormy"

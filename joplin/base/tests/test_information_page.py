from pages.information_page.models import InformationPageContact
from base.factories.information_page import InformationPageContactFactory, InformationPageFactory
import pytest


@pytest.mark.django_db
def test_information_page_factory(information_page_factory):
    page = information_page_factory.build(description="Dark and stormy")
    assert page.description == "Dark and stormy"


"""
example of a model based test but this currently dosen't work with our setup
@pytest.mark.django_db
@pytest.mark.parametrize("information_page__description", ["Light an fluffy"])
def test_model_fixture(information_page):
    assert information_page.description == "Light an fluffy"
"""

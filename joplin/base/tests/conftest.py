from pytest_factoryboy import register
import pytest
import inspect
from factory.base import FactoryMetaClass
from base.factories.information_page import InformationPageContactFactory, InformationPageFactory
from base.factories import information_page, service_page, guide_page


def register_factories(factories):
    """
    lil loop to go through and register factory objects
    like this:
    register(InformationPageContactFactory)
    register(InformationPageFactory)
    but without having to write them all out
    """
    for name, object in inspect.getmembers(factories):
        if isinstance(object, FactoryMetaClass) and not object._meta.abstract:
            register(object)


register_factories(information_page)
register_factories(service_page)
register_factories(guide_page)

# example if we wanted to make a specific fixture for some tests
# @pytest.fixture()
# def information_page(information_page_factory):
#     return InformationPageFactory.build()

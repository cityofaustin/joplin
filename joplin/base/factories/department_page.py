import factory
import wagtail_factories
from base.models import *
from .shared_factories import PageFactory

"""
DepartmentPage
DepartmentPageDirector
DepartmentPageContact
DepartmentPageTopPage
DepartmentPageRelatedPage
"""


class DepartmentPageFactory(PageFactory):

    mission = factory.Faker('text')

    class Meta:
        model = base.models.DepartmentPage

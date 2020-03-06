import factory
import wagtail_factories
from pages.factory import PageFactory

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
        model = pages.department_page.DepartmentPage

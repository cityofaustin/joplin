import factory
from pages.department_page.models import DepartmentPage
from pages.factory import PageFactory


class DepartmentPageFactory(PageFactory):

    mission = factory.Faker('text')

    class Meta:
        model = DepartmentPage

from pages.department_page.models import DepartmentPage
from pages.factory import PageFactory


class DepartmentPageFactory(PageFactory):
    class Meta:
        model = DepartmentPage

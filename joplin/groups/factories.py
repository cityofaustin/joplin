import factory
import wagtail_factories
from groups.models import Department


class DepartmentFactory(wagtail_factories.factories.MP_NodeFactory):
    department_page = factory.SubFactory('department_page.DepartmentPageFactory')

    class Meta:
        model = Department

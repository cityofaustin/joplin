import factory
from groups.models import Department
from wagtail.core.models import GroupPagePermission


class DepartmentFactory(factory.DjangoModelFactory):
    department_page = factory.SubFactory('pages.department_page.factories.DepartmentPageFactory')
    name = factory.Sequence(lambda n: f'Test Department {n}')

    class Meta:
        model = Department


class GroupPagePermissionFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base_page.factories.JanisBasePageFactory')
    group = factory.SubFactory(DepartmentFactory)

    class Meta:
        model = GroupPagePermission

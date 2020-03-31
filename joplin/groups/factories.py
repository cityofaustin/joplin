import factory
from groups.models import Department
from wagtail.core.models import GroupPagePermission


class DepartmentFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'Test Department {n}')

    class Meta:
        model = Department

    @factory.post_generation
    def add_department_page(self, create, extracted, **kwargs):
        # pass "add_department_page__dummy"=True into Factory() to make dummy department page
        if create:
            if (kwargs.get("dummy", False)):
                department_page = factory.SubFactory('pages.department_page.factories.DepartmentPageFactory')
                # TODO, add it to group


class GroupPagePermissionFactory(factory.django.DjangoModelFactory):
    page = factory.SubFactory('base_page.factories.JanisBasePageFactory')
    group = factory.SubFactory(DepartmentFactory)

    class Meta:
        model = GroupPagePermission

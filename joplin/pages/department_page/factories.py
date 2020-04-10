import factory
from pages.department_page.models import DepartmentPage, DepartmentPageDirector
from pages.base_page.factories import JanisBasePageFactory


class DepartmentPageDirectorFactory(factory.DjangoModelFactory):
    page = factory.SubFactory(
        'department_page.factories.DepartmentPageFactory',
    )

    class Meta:
        model = DepartmentPageDirector


class DepartmentPageFactory(JanisBasePageFactory):
    class Meta:
        model = DepartmentPage

    @factory.post_generation
    def add_department_directors(self, create, extracted, **kwargs):
        if extracted:
            # A list of topics were passed in, use them
            for director in extracted['department_directors']:
                DepartmentPageDirectorFactory.create(page=self, **director)
            return

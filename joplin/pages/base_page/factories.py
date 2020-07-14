import factory
from pages.factory import PageFactory
from pages.base_page.models import JanisBasePage


class JanisBasePageFactory(PageFactory):
    class Meta:
        model = JanisBasePage

    @factory.post_generation
    def add_departments(self, create, extracted, **kwargs):
        # Import here to avoid circular dependencies for the DepartmentPage
        from groups.factories import GroupPagePermissionFactory

        if extracted:
            # A list of departments were passed in, use them
            for department in extracted['departments']:
                GroupPagePermissionFactory.create(page=self, group=department, permission_type='edit')
            return

        # pass "add_departments__dummy"=True into Factory() to make dummy departments
        if create:
            if kwargs.get("dummy", False):
                GroupPagePermissionFactory.create(page=self)

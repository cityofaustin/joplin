import factory
from groups.models import Department
from pages.factory import PageFactory
from pages.base_page.models import JanisBasePage


class JanisBasePageFactory(PageFactory):
    class Meta:
        model = JanisBasePage


    @factory.post_generation
    def add_departments(self, create, extracted, **kwargs):
        # Import here to avoid circular dependencies for the DepartmentPage
        from groups.factories import GroupPagePermissionFactory

        # TODO: add option to pass in already created departments
        if extracted:
            # A list of departments were passed in, use them
            for department in extracted['departments']:
                # Check if a department with the same ????? has already been imported
                try:
                    # todo: create department groups
                    # slug we want to make is kitchen-sink-department
                    department_group = Department.objects.get(department_page__slug=department.slug)
                    document = Document.objects.get(file_hash=file_hash)
                except Document.DoesNotExist:
                    document = None
                if document:
                    return document

                # It has not been imported, let's do it!
                document = DocumentFactory.create(file=ContentFile(response.content, name=file_name), title=file_name)
                return document




                GroupPagePermissionFactory.create(page=self, )
            return


            # for related_department in extracted:
                # todo: add department stuff here
                # GroupPagePermissionFactory.create(page=self, topic_collection=topic_collection)
            return

        # pass "add_department__dummy"=True into Factory() to make dummy departments
        if create:
            if (kwargs.get("dummy", False)):
                GroupPagePermissionFactory.create(page=self)

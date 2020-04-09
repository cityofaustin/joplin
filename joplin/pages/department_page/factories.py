import factory
from pages.department_page.models import DepartmentPage
from pages.factory import PageFactory
from snippets.contact.factories import create_contact_from_importer_dictionaries
from pages.home_page.models import HomePage


class DepartmentPageFactory(PageFactory):
    mission = factory.Faker('text')

    class Meta:
        model = DepartmentPage


def create_department_page_from_importer_dictionaries(page_dictionaries, revision_id):
    # first check to see if we already imported this page
    # if we did, just go to the edit page for it without changing the db
    # todo: maybe change this to allow updating pages in the future?
    try:
        page = DepartmentPage.objects.get(imported_revision_id=revision_id)
    except DepartmentPage.DoesNotExist:
        page = None
    if page:
        return page

    # since we don't have a page matching the revision id, we should look
    # for other matches, for now let's just use english slug
    # todo: figure out what we want the logic around importing a page with the same slug to look like
    try:
        page = DepartmentPage.objects.get(slug=page_dictionaries['en']['slug'])
    except DepartmentPage.DoesNotExist:
        page = None
    if page:
        return page

    # since we don't have a page matching the revision id or the slug
    # make the combined page dictionary
    combined_dictionary = page_dictionaries['en']

    # associate/create contact
    if len(page_dictionaries['en']['contacts']['edges']):
        combined_dictionary['contact'] = create_contact_from_importer_dictionaries(page_dictionaries)

    # remove contacts if we have it because:
    # * we just added it up above
    # todo: why isn't pop working?
    if 'contacts' in combined_dictionary:
        del combined_dictionary['contacts']

    #  todo: get department directors working
    # remove directors if we have it because:
    # * we just added it up above todo actually add it up above
    # todo: why isn't pop working?
    if 'department_directors' in combined_dictionary:
        del combined_dictionary['department_directors']

    # Set home as parent
    combined_dictionary['parent'] = HomePage.objects.first()

    # set the translated fields
    for field in DepartmentPageFactory._meta.model._meta.fields:
        if field.column.endswith("_es"):
            if field.column[:-3] in page_dictionaries['es']:
                combined_dictionary[field.column] = page_dictionaries['es'][field.column[:-3]]

    page = DepartmentPageFactory.create(**combined_dictionary)
    return page



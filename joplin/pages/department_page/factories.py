import factory
from pages.department_page.models import DepartmentPage, DepartmentPageDirector
from pages.factory import PageFactory
from snippets.contact.factories import create_contact_from_importer_dictionaries
from pages.home_page.models import HomePage


class DepartmentPageDirectorFactory(factory.DjangoModelFactory):
    page = factory.SubFactory(
        'department_page.factories.DepartmentPageFactory',
    )

    class Meta:
        model = DepartmentPageDirector


class DepartmentPageFactory(PageFactory):
    class Meta:
        model = DepartmentPage

    @factory.post_generation
    def add_department_directors(self, create, extracted, **kwargs):
        if extracted:
            # A list of topics were passed in, use them
            for director in extracted['department_directors']:
                DepartmentPageDirectorFactory.create(page=self, **director)
            return


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

    # create/associate department directors
    department_directors = []
    for index in range(len(page_dictionaries['en']['department_directors']['edges'])):
        en_node = page_dictionaries['en']['department_directors']['edges'][index]['node']
        es_node = page_dictionaries['es']['department_directors']['edges'][index]['node']

        combined_node = en_node
        combined_node['title_es'] = es_node['title']
        combined_node['about_es'] = es_node['about']

        department_directors.append(combined_node)
    combined_dictionary['add_department_directors'] = {'department_directors': department_directors}

    # remove directors if we have it because:
    # * we just added it up above
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



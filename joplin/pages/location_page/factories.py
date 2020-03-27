import json
from pages.base_page.factories import JanisBasePageFactory
from pages.home_page.models import HomePage
from pages.location_page.models import LocationPage


class LocationPageFactory(JanisBasePageFactory):
    @classmethod
    def create(cls, *args, **kwargs):
        # todo: figure out what goes here
        # Convert steps into StreamField-parseable json dump
        # step_keywords = ['steps', 'steps_es']
        # for step_keyword in step_keywords:
        #     steps = kwargs.pop(step_keyword, [])
        #     formatted_steps = json.dumps([
        #         {
        #             u'type': u'{0}'.format(step['type']),
        #             u'value': u'{0}'.format(step['value'])
        #         }
        #         for step in steps
        #     ])
        #     kwargs[step_keyword] = formatted_steps
        return super(LocationPageFactory, cls).create(*args, **kwargs)


    class Meta:
        model = LocationPage


# decamelize gives us time2 instead of time_2
# let's go aheead and recursively fix that
def fix_nums(k): return k.translate(str.maketrans({'1': '_1', '2': '_2', '3': '_3'}))


def change_keys(obj, convert):
    """
    Recursively goes through the dictionary obj and replaces keys with the convert function.
    """
    if isinstance(obj, (str, int, float)):
        return obj
    if isinstance(obj, dict):
        new = obj.__class__()
        for k, v in obj.items():
            new[convert(k)] = change_keys(v, convert)
    elif isinstance(obj, (list, set, tuple)):
        new = obj.__class__(change_keys(v, convert) for v in obj)
    else:
        return obj
    return new


def create_location_page_from_importer_dictionaries(page_dictionaries, revision_id=None):
    # Check if page with revision_id has already been imported
    if revision_id:
        try:
            page = LocationPage.objects.get(imported_revision_id=revision_id)
        except LocationPage.DoesNotExist:
            page = None
        if page:
            return page

    # Check if page with (english) slug has already been imported
    try:
        page = LocationPage.objects.get(slug=page_dictionaries['en']['slug'])
    except LocationPage.DoesNotExist:
        page = None
    if page:
        return page

    # since we don't have a page matching the revision id or the slug
    # make the combined page dictionary
    combined_dictionary = page_dictionaries['en']

    # Set home as parent
    combined_dictionary['parent'] = HomePage.objects.first()

    # set the translated fields
    for field in LocationPageFactory._meta.model._meta.fields:
        if field.column.endswith("_es"):
            if field.column[:-3] in page_dictionaries['es']:
                combined_dictionary[field.column] = page_dictionaries['es'][field.column[:-3]]

    # fix them up for our bus_2 and time_2 needs (instead of time2 bus2)
    combined_dictionary = change_keys(combined_dictionary, fix_nums)

    # todo: maybe get this related service logic working
    # # for now, just get the title from the page on related service and clear it out
    # for edge in combined_dictionary['related_services']['edges']:
    #     edge['node']['hours_exceptions'] += edge['node']['related_service']['title']
    #     del edge['node']['related_service']

    page = LocationPageFactory.create(**combined_dictionary)
    return page

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

    # remove contacts if we have it because:
    # * it might be what's wrong rn
    # todo: why isn't pop working?
    if 'contacts' in combined_dictionary:
        del combined_dictionary['contacts']

    # Set home as parent
    combined_dictionary['parent'] = HomePage.objects.first()

    # set the translated fields
    for field in LocationPageFactory._meta.model._meta.fields:
        if field.column.endswith("_es"):
            if field.column[:-3] in page_dictionaries['es']:
                combined_dictionary[field.column] = page_dictionaries['es'][field.column[:-3]]


    # todo: actually get departments here
    # combined_dictionary['add_related_departments'] = ['just a string']

    page = LocationPageFactory.create(**combined_dictionary)
    return page

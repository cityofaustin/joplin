import factory
from pages.base_page.factories import JanisBasePageFactory
from pages.home_page.models import HomePage
# from pages.service_page.models import ServicePage
# from pages.service_page.factories import ServicePageFactory
# from pages.location_page.models import LocationPage, LocationPageRelatedServices
from pages.event_page.models import EventPage


# class LocationPageRelatedServicesFactory(factory.django.DjangoModelFactory):
#     page = factory.SubFactory('pages.location_page.factories.LocationPageFactory')
#     related_service = factory.SubFactory('pages.service_page.factories.ServicePageFactory')
#
#     class Meta:
#         model = LocationPageRelatedServices


class EventPageFactory(JanisBasePageFactory):
    # @classmethod
    # def create(cls, *args, **kwargs):
    #     return super(EventPageFactory, cls).create(*args, **kwargs)

    # @factory.post_generation
    # def add_related_services(self, create, extracted, **kwargs):
    #     if extracted:
    #         # A list of related services were passed in,
    #         # this includes info about hours for the related service
    #         for Event_page_related_service in extracted:
    #             EventPageRelatedServicesFactory.create(page=self, **event_page_related_service)
    #         return

    class Meta:
        model = EventPage

def create_event_page_from_importer_dictionaries(page_dictionaries, revision_id):
    # first check to see if we already imported this page
    # if we did, just go to the edit page for it without changing the db
    # todo: maybe change this to allow updating pages in the future?
    try:
        page = EventPage.objects.get(imported_revision_id=revision_id)
    except EventPage.DoesNotExist:
        page = None
    if page:
        return page

    # since we don't have a page matching the revision id, we should look
    # for other matches, for now let's just use english slug
    # todo: figure out what we want the logic around importing a page with the same slug to look like
    try:
        page = EventPage.objects.get(slug=page_dictionaries['en']['slug'])
    except EventPage.DoesNotExist:
        page = None
    if page:
        return page

    # since we don't have a page matching the revision id or the slug
    # make the combined page dictionary
    combined_dictionary = page_dictionaries['en']

    # todo: figure out where to move this so it isn't copypasta in service page
    # # associate/create topic pages
    # topic_pages = []
    # for index in range(len(page_dictionaries['en']['topics']['edges'])):
    #     topic_pages.append(create_topic_page_from_importer_dictionaries({
    #         'en': page_dictionaries['en']['topics']['edges'][index]['node']['topic'],
    #         'es': page_dictionaries['es']['topics']['edges'][index]['node']['topic'],
    #     }, page_dictionaries['en']['topics']['edges'][index]['node']['topic']['live_revision']['id']))
    # combined_dictionary['add_topics'] = {'topics': topic_pages}

    # remove topics if we have it because:
    # * it's in english only
    # * the factory doesn't know what to do with it
    # # todo: why isn't pop working?
    # if 'topics' in combined_dictionary:
    #     del combined_dictionary['topics']

    # remove contacts if we have it because:
    # * it might be what's wrong rn
    # todo: why isn't pop working?
    # if 'contacts' in combined_dictionary:
    #     del combined_dictionary['contacts']


    # Set home as parent
    combined_dictionary['parent'] = HomePage.objects.first()

    # set the translated fields
    for field in EventPageFactory._meta.model._meta.fields:
        if field.column.endswith("_es"):
            if field.column[:-3] in page_dictionaries['es']:
                combined_dictionary[field.column] = page_dictionaries['es'][field.column[:-3]]

    # todo: actually get departments here
    # combined_dictionary['add_department'] = ['just a string']

    page = EventPageFactory.create(**combined_dictionary)
    return page


#
# # decamelize gives us time2 instead of time_2
# # let's go ahead and recursively fix that
# def fix_nums(k): return k.translate(str.maketrans({'1': '_1', '2': '_2', '3': '_3'}))
#
#
# def change_keys(obj, convert):
#     """
#     Recursively goes through the dictionary obj and replaces keys with the convert function.
#     """
#     if isinstance(obj, (str, int, float)):
#         return obj
#     if isinstance(obj, dict):
#         new = obj.__class__()
#         for k, v in obj.items():
#             new[convert(k)] = change_keys(v, convert)
#     elif isinstance(obj, (list, set, tuple)):
#         new = obj.__class__(change_keys(v, convert) for v in obj)
#     else:
#         return obj
#     return new
#
#
# def create_location_page_from_importer_dictionaries(page_dictionaries, revision_id=None):
#     # Check if page with revision_id has already been imported
#     if revision_id:
#         try:
#             page = LocationPage.objects.get(imported_revision_id=revision_id)
#         except LocationPage.DoesNotExist:
#             page = None
#         if page:
#             return page
#
#     # Check if page with (english) slug has already been imported
#     try:
#         page = LocationPage.objects.get(slug=page_dictionaries['en']['slug'])
#     except LocationPage.DoesNotExist:
#         page = None
#     if page:
#         return page
#
#     # since we don't have a page matching the revision id or the slug
#     # make the combined page dictionary
#     combined_dictionary = page_dictionaries['en']
#
#     # Set home as parent
#     combined_dictionary['parent'] = HomePage.objects.first()
#
#     # set the translated fields
#     for field in LocationPageFactory._meta.model._meta.fields:
#         if field.column.endswith("_es"):
#             if field.column[:-3] in page_dictionaries['es']:
#                 combined_dictionary[field.column] = page_dictionaries['es'][field.column[:-3]]
#
#     # fix them up for our bus_2 and time_2 needs (instead of time2 bus2)
#     combined_dictionary = change_keys(combined_dictionary, fix_nums)
#
#     # todo: maybe get this related service logic working
#     # # for now, just get the title from the page on related service and clear it out
#     combined_dictionary['add_related_services'] = []
#     for edge in combined_dictionary['related_services']['edges']:
#         location_page_related_service_to_add = edge['node']
#
#         # since we're using a placeholder service, let's at least get the title somewhere to help us find the page
#         location_page_related_service_to_add['hours_exceptions'] += location_page_related_service_to_add['related_service']['title']
#
#         # We really are just trying to get hours imported here, but we can't save
#         # without having a page FK'd out to, so we use a placeholder service for now.
#         # In order to update this, we'll need to go into the location page and manually update the related service
#         # Check if page with (english) slug has already been imported
#         try:
#             related_service = ServicePage.objects.get(slug='placeholder_service_for_hours')
#         except ServicePage.DoesNotExist:
#             related_service = None
#         if not related_service:
#             related_service_dictionary = {
#                 'parent': combined_dictionary['parent'],
#                 'title': 'placeholder service for hours',
#                 'slug': 'placeholder_service_for_hours'
#             }
#             related_service = ServicePageFactory.create(**related_service_dictionary)
#         del location_page_related_service_to_add['related_service']
#         location_page_related_service_to_add['related_service'] = related_service
#         combined_dictionary['add_related_services'].append(location_page_related_service_to_add)
#     del combined_dictionary['related_services']
#
#     page = LocationPageFactory.create(**combined_dictionary)
#     return page

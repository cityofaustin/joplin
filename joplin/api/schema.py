import django.utils.translation
import graphene
from django.core.exceptions import ObjectDoesNotExist
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField
from graphene.types import Scalar
from graphene.types.json import JSONString
from graphene.types.generic import GenericScalar
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import PageRevision
from django_filters import FilterSet, OrderingFilter
from wagtail.core.blocks import *
from wagtail.documents.models import Document
from wagtail.core.rich_text import expand_db_html
from base.models import (
    TranslatedImage,
    ServicePage, ServicePageContact, ServicePageTopic, ServicePageRelatedDepartments,
    InformationPage, InformationPageContact, InformationPageTopic, InformationPageRelatedDepartments,
    DepartmentPage, DepartmentPageContact, DepartmentPageDirector, DepartmentPageTopPage, DepartmentPageRelatedPage,
    Theme, TopicCollectionPage, TopicPage, TopicPageTopicCollection, TopicPageTopPage,
    Contact, Location, PhoneNumber, ContactDayAndDuration, Department, DepartmentContact,
    OfficialDocumentPage, OfficialDocumentPageRelatedDepartments, OfficialDocumentPageTopic, OfficialDocumentPageOfficialDocument,
    GuidePage, GuidePageTopic, GuidePageRelatedDepartments, GuidePageContact,
    FormContainer, FormContainerRelatedDepartments, FormContainerTopic,
)
from .content_type_map import content_type_map
import traceback
from locations.models import LocationPage, LocationPageRelatedServices
from events.models import EventPage, EventPageFee, EventPageRelatedDepartments
from graphql_relay import to_global_id


class RichTextFieldType(Scalar):
    """
    Serialises RichText content into fully baked HTML
    see https://github.com/wagtail/wagtail/issues/2695#issuecomment-464462575
    """
    @staticmethod
    def serialize(value):
        return expand_db_html(value)


@convert_django_field.register(RichTextField)
def convert_rich_text_field(field, registry=None):
    return RichTextFieldType(
        description=field.help_text, required=not field.null
    )


def try_expand_db_html(parsed_item):
    """
    expand_db_html errors out if not used on a string.
    becuase this process is so complicated, we wrap it in some error handiling
    so we can debug/catch an exception if someone adds a data schema later
    that causes problems
    """
    try:
        return expand_db_html(parsed_item)
    except Exception as e:
        print('try_expand_db_html!', e)
        print(traceback.format_exc())
        return parsed_item


def expand_dict_values(item):
    """
    dict comprehension that expands db html on each item in a dict
    """
    if isinstance(item, int):
        return item
    try:
        dict_values = {key: try_expand_db_html(value) for (key, value) in item.items() if item is not isinstance(item, int)}
        return dict_values
    except Exception as e:
        print('dict_comprehension error!', e)
        print(traceback.format_exc())


def expand_by_type(key, value):
    """
    recursive function to
    handle the streamfield block items differently depending on type
    and loop through again if its a dict
    """
    if isinstance(value, str):
        parsed_item = try_expand_db_html(value)
        return parsed_item
    elif isinstance(value, list):
        parsed_item = [expand_dict_values(item) for item in value]
        return parsed_item
    elif isinstance(value, dict):
        try_get_api_representation(value)


def try_get_api_representation(StreamChild):
    if StreamChild.block_type == "map_block":
        # this has its own representation definition in blocks.py
        block = StreamChild.block.get_api_representation(StreamChild.value)
        return block

    try:
        if not isinstance(StreamChild, dict):
            block = StreamChild.block.get_api_representation(StreamChild.value) or None
        # if the block is just a string (no dict at all), just return it expanded
            if isinstance(block, str):
                parsed_block = try_expand_db_html(block)
                return parsed_block
            elif StreamChild.block_type == "step_with_locations":
                block = StreamChild.block.get_api_representation(StreamChild.value)
                location_pages = StreamChild.value['locations']

                for index, location_page in enumerate(location_pages):
                    # cast as node so we can get the global id
                    lp = LocationPageNode(location_page)
                    parsed_location = {
                        "locationPage": {
                            "id": to_global_id(lp._meta.name, location_page.id),
                            "slug": location_page.slug,
                            "title": location_page.title,
                            "physicalStreet": location_page.physical_street,
                            "physicalUnit": location_page.physical_unit,
                            "physicalCity": location_page.physical_city,
                            "physicalState": location_page.physical_state,
                            "physicalZip": location_page.physical_zip,
                        }
                    }
                    # replace the pk entry in the StreamChild output with the parsed info above
                    block['locations'][index] = parsed_location
                    block['locations_description'] = expand_db_html(block['locations_description'])
                return block
            elif isinstance(block, dict):
                parsed_block = {key: expand_by_type(key, value) for (key, value) in block.items()}
                return parsed_block
    except Exception as e:
        print('try_get_api_representation!', e)
        print(traceback.format_exc())


class StreamFieldType(Scalar):
    @staticmethod
    def serialize(StreamValue):
        """
        Returns Streamfields for the api, also expanding db html to make sure links work
        """
        expanded_streamfields = [
            {
                'type': StreamChild.block_type,
                'value': try_get_api_representation(StreamChild),
                'id': StreamChild.id
            } for StreamChild in StreamValue
        ]
        return expanded_streamfields


@convert_django_field.register(StreamField)
def convert_stream_field(field, registry=None):
    return StreamFieldType(description=field.help_text, required=not field.null)


class DocumentNode(DjangoObjectType):
    class Meta:
        model = Document
        interfaces = [graphene.Node]
        exclude_fields = ['tags']
    filename = graphene.String()


class ThemeNode(DjangoObjectType):
    class Meta:
        model = Theme
        filter_fields = ['id', 'slug', 'text']
        interfaces = [graphene.Node]


class TopicCollectionNode(DjangoObjectType):
    class Meta:
        model = TopicCollectionPage
        filter_fields = ['id', 'slug', 'live']
        interfaces = [graphene.Node]


class TopicPageTopicCollectionNode(DjangoObjectType):
    class Meta:
        model = TopicPageTopicCollection
        interfaces = [graphene.Node]
        filter_fields = ['topiccollection']


class TopicNode(DjangoObjectType):
    class Meta:
        model = TopicPage
        filter_fields = ['id', 'slug', 'live']
        interfaces = [graphene.Node]


class DepartmentNode(DjangoObjectType):
    class Meta:
        model = Department
        filter_fields = ['id', 'name']
        interfaces = [graphene.Node]


class DepartmentContactNode(DjangoObjectType):
    class Meta:
        model = DepartmentContact
        interfaces = [graphene.Node]


class LocationNode(DjangoObjectType):
    class Meta:
        model = Location
        filter_fields = ['id']
        fields = '__all__'
        interfaces = [graphene.Node]


class LocationPageNode(DjangoObjectType):
    class Meta:
        model = LocationPage
        filter_fields = ['id', 'slug', 'live']
        fields = '__all__'
        interfaces = [graphene.Node]


class LocationPageRelatedServices(DjangoObjectType):
    class Meta:
        model = LocationPageRelatedServices
        fields = '__all__'
        interfaces = [graphene.Node]


class EventFilter(FilterSet):
    order_by = OrderingFilter(
        fields=(
            ('date'),
        )
    )

    class Meta:
        model = EventPage
        fields = {
            'date': ['exact', 'lte', 'gte'],
            'live': ['exact']
        }


class EventPageRemoteLocation(graphene.ObjectType):
    """
    Remote Location = non city owned location
    """
    value = GenericScalar()

    street = graphene.String()
    unit = graphene.String()
    city = graphene.String()
    state = graphene.String()
    zip = graphene.String()

    def resolve_street(self, info):
        return self.value['street']

    def resolve_unit(self, info):
        return self.value['unit']

    def resolve_city(self, info):
        return self.value['city']

    def resolve_state(self, info):
        return self.value['state']

    def resolve_zip(self, info):
        return self.value['zip']

    name = graphene.String()

    def resolve_name(self, info):
        # We're doing our own translations in our model here
        # so let's make sure the API returns the appropriate name for:
        '''
        remoteLocation {
            name
        }
        '''
        # based on the Accept-Language header of the request
        if django.utils.translation.get_language() == 'en':
            return self.value['name_en']
        elif django.utils.translation.get_language() == 'es':
            # if there is not a spanish translation available, return english
            if self.value['name_es'] == '':
                return self.value['name_en']
            return self.value['name_es']
        elif django.utils.translation.get_language() == 'ar':
            return self.value['name_ar']
        elif django.utils.translation.get_language() == 'vi':
            return self.value['name_vi']


# In order to support "pick city or not but not both" functionality:
# While only displaying the relevant fields for the selected type
# We decided on using streamfields and setting up a max_num in them
# https://github.com/cityofaustin/techstack/issues/3851
#
# A custom resolver is needed to make streamfields queryable
# so if we want the API to support queries like:
"""

eventPage {
    location {
        city_location {
            physicalLocation
        }
    }
}
"""
# instead of just getting predetermined fields back from queries like:
"""
eventPage {
    location
}
"""
# we need to use a custom resolver
# we could also try to make our streamfield type queryable,
# but that is a rabbit hole I haven't jumped all the way down yet


class EventPageLocation(graphene.ObjectType):
    value = GenericScalar()
    location_type = graphene.String()
    additional_details = graphene.String()
    city_location = graphene.Field(LocationPageNode)
    remote_location = graphene.Field(EventPageRemoteLocation)

    def resolve_additional_details(self, info):
        # We're doing our own translations in our model here
        # so let's make sure the API still works as expected
        if django.utils.translation.get_language() == 'en':
            return self.value['additional_details_en']
        elif django.utils.translation.get_language() == 'es':
            # if there is not a spanish translation available, return english
            if self.value['additional_details_es'] == '':
                return self.value['additional_details_en']
            return self.value['additional_details_es']
        elif django.utils.translation.get_language() == 'ar':
            return self.value['additional_details_ar']
        elif django.utils.translation.get_language() == 'vi':
            return self.value['additional_details_vi']

    def resolve_city_location(self, info):
        page = None
        if self.location_type == 'city_location':
            try:
                page = LocationPage.objects.get(id=self.value['location_page'])
            except ObjectDoesNotExist:
                pass
            return page

    def resolve_remote_location(self, info):
        if self.location_type == 'remote_location':
            return EventPageRemoteLocation(value=self.value)


class EventPageNode(DjangoObjectType):
    locations = graphene.List(EventPageLocation)

    class Meta:
        model = EventPage
        filter_fields =  ['id', 'slug', 'live', 'date']
        interfaces = [graphene.Node]

    def resolve_locations(self, info):
        repr_locations = []
        for block in self.location_blocks.stream_data:
            value = block.get('value')
            location_type = block.get('type')
            repr_locations.append(EventPageLocation(value=value, location_type=location_type))

        return repr_locations


class EventPageFeeNode(DjangoObjectType):
    class Meta:
        model = EventPageFee
        interfaces = [graphene.Node]


class EventPageRelatedDepartmentsNode(DjangoObjectType):
    class Meta:
        model = EventPageRelatedDepartments
        interfaces = [graphene.Node]


class ContactNode(DjangoObjectType):
    class Meta:
        model = Contact
        interfaces = [graphene.Node]


class ContactPhoneNumbers(DjangoObjectType):
    class Meta:
        model = PhoneNumber
        interfaces = [graphene.Node]


class ContactDayAndDurationNode(DjangoObjectType):
    class Meta:
        model = ContactDayAndDuration
        interfaces = [graphene.Node]


class ServicePageContactNode(DjangoObjectType):
    class Meta:
        model = ServicePageContact
        interfaces = [graphene.Node]


class GuidePageContactNode(DjangoObjectType):
    class Meta:
        model = GuidePageContact
        interfaces = [graphene.Node]


class ServicePageTopicNode(DjangoObjectType):
    class Meta:
        model = ServicePageTopic
        interfaces = [graphene.Node]
        filter_fields = ['topic']


class ServicePageRelatedDepartmentsNode(DjangoObjectType):
    class Meta:
        model = ServicePageRelatedDepartments
        interfaces = [graphene.Node]


class InformationPageRelatedDepartmentsNode(DjangoObjectType):
    class Meta:
        model = InformationPageRelatedDepartments
        interfaces = [graphene.Node]


class OfficialDocumentPageRelatedDepartmentsNode(DjangoObjectType):
    class Meta:
        model = OfficialDocumentPageRelatedDepartments
        interfaces = [graphene.Node]


class GuidePageRelatedDepartmentsNode(DjangoObjectType):
    class Meta:
        model = GuidePageRelatedDepartments
        interfaces = [graphene.Node]


class FormContainerRelatedDepartmentsNode(DjangoObjectType):
    class Meta:
        model = FormContainerRelatedDepartments
        interfaces = [graphene.Node]


class TranslatedImageNode(DjangoObjectType):
    class Meta:
        model = TranslatedImage
        interfaces = [graphene.Node]
        exclude_fields = ['tags']
    filename = graphene.String()


class Language(graphene.Enum):
    ENGLISH = 'en'
    SPANISH = 'es'
    VIETNAMESE = 'vi'
    CHINESE_SIMPLE = 'zh-hans'
    CHINESE_TRADITIONAL = 'zh-hant'
    ARABIC = 'ar'
    KOREAN = 'ko'
    URDU = 'ur'
    BURMESE = 'my'


class ServicePageNode(DjangoObjectType):
    page_type = graphene.String()
    janis_url = graphene.String()

    class Meta:
        model = ServicePage
        filter_fields = ['id', 'slug', 'live', 'coa_global']
        interfaces = [graphene.Node]

    def resolve_page_type(self, info):
        return ServicePage.get_verbose_name().lower()

    def resolve_janis_url(self, info):
        return self.janis_url()


class InformationPageNode(DjangoObjectType):
    page_type = graphene.String()

    class Meta:
        model = InformationPage
        filter_fields = ['id', 'slug', 'live', 'coa_global']
        interfaces = [graphene.Node]

    def resolve_page_type(self, info):
        return InformationPage.get_verbose_name().lower()


class DepartmentPageNode(DjangoObjectType):
    page_type = graphene.String()

    class Meta:
        model = DepartmentPage
        filter_fields = ['id', 'slug', 'live']
        interfaces = [graphene.Node]

    def resolve_page_type(self, info):
        return DepartmentPage.get_verbose_name().lower()


class FormContainerNode(DjangoObjectType):
    page_type = graphene.String()

    class Meta:
        model = FormContainer
        filter_fields = ['id', 'slug', 'live', 'coa_global']
        interfaces = [graphene.Node]

    def resolve_page_type(self, info):
        return FormContainer.get_verbose_name().lower()


class OfficialDocumentFilter(FilterSet):
    order_by = OrderingFilter(
        fields=(
            ('date'),
        )
    )

    class Meta:
        model = OfficialDocumentPageOfficialDocument
        fields = ['date']


class OfficialDocumentPageOfficialDocumentNode(DjangoObjectType):
    class Meta:
        model = OfficialDocumentPageOfficialDocument
        filter_fields = ['date']
        interfaces = [graphene.Node]


class OfficialDocumentPageNode(DjangoObjectType):
    page_type = graphene.String()
    official_documents = DjangoFilterConnectionField(
        OfficialDocumentPageOfficialDocumentNode, filterset_class=OfficialDocumentFilter)

    class Meta:
        model = OfficialDocumentPage
        filter_fields = ['id', 'slug', 'live', 'coa_global']
        interfaces = [graphene.Node]

    def resolve_page_type(self, info):
        return OfficialDocumentPage.get_verbose_name().lower()


def resolve_guide_page_section_as(model, self):
    page = None
    try:
        page = model.objects.get(id=self.value)
    except ObjectDoesNotExist:
        pass
    return page


class GuidePageSectionPageBlock(graphene.ObjectType):
    # This uses graphene ObjectType resolvers, see:
    # https://docs.graphene-python.org/en/latest/types/objecttypes/#resolvers

    value = GenericScalar()
    url = graphene.String()
    service_page = graphene.Field(ServicePageNode)
    information_page = graphene.Field(InformationPageNode)
    form_container = graphene.Field(FormContainerNode)

    def __resolve_guide_page_section_as(self, model):
        page = None
        try:
            page = model.objects.get(id=self.value)
        except ObjectDoesNotExist:
            pass
        return page

    def resolve_url(self, resolve_info, *args, **kwargs):
        page = None
        for model in [
            ServicePage,
            InformationPage,
            FormContainer,
        ]:
            page = self.__resolve_guide_page_section_as(model)
            if page:
                break
        if page:
            return page.janis_url()
        else:
            return '#'

    def resolve_service_page(self, info):
        return self.__resolve_guide_page_section_as(ServicePage)

    def resolve_information_page(self, info):
        return self.__resolve_guide_page_section_as(InformationPage)

    def resolve_form_container(self, info):
        return self.__resolve_guide_page_section_as(FormContainer)


class GuidePageSection(graphene.ObjectType):
    value = GenericScalar()
    pages = graphene.List(GuidePageSectionPageBlock)
    heading = graphene.String()

    def resolve_heading(self, info):
        # We're doing our own translations in our model here
        # so let's make sure the API still works as expected
        if django.utils.translation.get_language() == 'en':
            return self.value['section_heading_en']
        elif django.utils.translation.get_language() == 'es':
            # if there is not a spanish translation available, return english
            if self.value['section_heading_es'] == '':
                return self.value['section_heading_en']
            return self.value['section_heading_es']
        elif django.utils.translation.get_language() == 'ar':
            return self.value['section_heading_ar']
        elif django.utils.translation.get_language() == 'vi':
            return self.value['section_heading_vi']

    def resolve_pages(self, info):
        repr_pages = []
        for page_id in self.value['pages']:
            repr_pages.append(GuidePageSectionPageBlock(value=page_id))

        return repr_pages


class GuidePageNode(DjangoObjectType):
    sections = graphene.List(GuidePageSection)
    page_type = graphene.String()

    class Meta:
        model = GuidePage
        filter_fields = ['id', 'slug', 'live', 'coa_global']
        interfaces = [graphene.Node]

    def resolve_sections(self, info):
        repr_sections = []
        for block in self.sections.stream_data:
            value = block.get('value')
            repr_sections.append(GuidePageSection(value=value))

        return repr_sections

    def resolve_page_type(self, info):
        return GuidePage.get_verbose_name().lower()


class PageRevisionNode(DjangoObjectType):
    as_service_page = graphene.NonNull(ServicePageNode)
    as_information_page = graphene.NonNull(InformationPageNode)
    as_department_page = graphene.NonNull(DepartmentPageNode)
    as_topic_page = graphene.NonNull(TopicNode)
    as_topic_collection_page = graphene.NonNull(TopicCollectionNode)
    as_official_document_page = graphene.NonNull(OfficialDocumentPageNode)
    as_guide_page = graphene.NonNull(GuidePageNode)
    as_form_container = graphene.NonNull(FormContainerNode)
    as_location_page = graphene.NonNull(LocationPageNode)
    as_event_page = graphene.NonNull(EventPageNode)

    def resolve_as_service_page(self, resolve_info, *args, **kwargs):
        return self.as_page_object()

    def resolve_as_information_page(self, resolve_info, *args, **kwargs):
        return self.as_page_object()

    def resolve_as_department_page(self, resolve_info, *args, **kwargs):
        return self.as_page_object()

    def resolve_as_topic_page(self, resolve_info, *args, **kwargs):
        return self.as_page_object()

    def resolve_as_topic_collection_page(self, resolve_info, *args, **kwargs):
        return self.as_page_object()

    def resolve_as_official_document_page(self, resolve_info, *args, **kwargs):
        return self.as_page_object()

    def resolve_as_guide_page(self, resolve_info, *args, **kwargs):
        return self.as_page_object()

    def resolve_as_form_container(self, resolve_info, *args, **kwargs):
        return self.as_page_object()

    def resolve_as_location_page(self, resolve_info, *args, **kwargs):
        return self.as_page_object()

    def resolve_as_event_page(self, resolve_info, *args, **kwargs):
        return self.as_page_object()

    class Meta:
        model = PageRevision
        filter_fields = ['id']
        interfaces = [graphene.Node]


def get_structure_for_content_type(content_type):
    site_structure = []
    content_type_data = content_type_map.get(content_type, None)
    if not content_type_data:
        raise Exception(f'content_type [{content_type}] is not included in content_type_map')

    pages = content_type_data["model"].objects.all()
    for page in pages:
        page_global_id = graphene.Node.to_global_id(content_type_data["node"], page.id)

        # Only publish event pages at the date based url
        if content_type == 'event page':
            if page.date:
                site_structure.append({'url': f'/event/{page.date.year}/{page.date.month}/{page.date.day}/{page.slug}/', 'type': content_type, 'id': page_global_id})
            continue

        if page.coa_global:
            site_structure.append({'url': f'/{page.slug}/', 'type': content_type, 'id': page_global_id})

        # For content_type models that have related departments
        if hasattr(page, "related_departments"):
            page_departments = page.related_departments.all()
            for page_department in page_departments:
                page_department_global_id = graphene.Node.to_global_id('DepartmentNode', page_department.related_department.id)
                site_structure.append({'url': f'/{page_department.related_department.slug}/{page.slug}/', 'type': content_type, 'id': page_global_id, 'parent_department': page_department_global_id})

        # For content_type models that have topics
        if hasattr(page, "topics"):
            page_topics = page.topics.all()
            for page_topic in page_topics:
                page_topic_global_id = graphene.Node.to_global_id('TopicNode', page_topic.topic.id)
                page_topic_tcs = page_topic.topic.topiccollections.all()
                for tc in page_topic_tcs:
                    if not tc.topiccollection.theme:
                        continue

                    page_topic_tc_global_id = graphene.Node.to_global_id('TopicCollectionNode', tc.topiccollection.id)
                    site_structure.append({'url': f'/{tc.topiccollection.theme.slug}/{tc.topiccollection.slug}/{page_topic.topic.slug}/{page.slug}/', 'type': content_type, 'id': page_global_id, 'parent_topic': page_topic_global_id, 'grandparent_topic_collection': page_topic_tc_global_id})

        # Location pages need urls
        if content_type == 'location page':
            site_structure.append({'url': f'/location/{page.slug}/', 'type': content_type, 'id': page_global_id})

    return site_structure


class SiteStructure(graphene.ObjectType):
    value = GenericScalar()
    structure_json = JSONString()

    # json isn't a great way to do this, we should
    # figure out how to make it queryable
    def resolve_structure_json(self, resolve_info, *args, **kwargs):
        # our structure here can be id: page dict
        site_structure = []
        topic_collections = TopicCollectionPage.objects.all()
        for topic_collection in topic_collections:
            if not topic_collection.theme:
                continue

            topic_collection_global_id = graphene.Node.to_global_id('TopicCollectionNode', topic_collection.id)
            site_structure.append({'url': f'/{topic_collection.theme.slug}/{topic_collection.slug}/', 'type': 'topic collection', 'id': topic_collection_global_id})

        topics = TopicPage.objects.all()
        for topic in topics:
            topic_global_id = graphene.Node.to_global_id('TopicNode', topic.id)
            topic_tcs = topic.topiccollections.all()
            for tc in topic_tcs:
                if not tc.topiccollection.theme:
                    continue

                topic_tc_global_id = graphene.Node.to_global_id('TopicCollectionNode', tc.topiccollection.id)
                site_structure.append({'url': f'/{tc.topiccollection.theme.slug}/{tc.topiccollection.slug}/{topic.slug}/', 'type': 'topic', 'id': topic_global_id, 'parent_topic_collection': topic_tc_global_id})

        departments = DepartmentPage.objects.all()
        for department in departments:
            department_global_id = graphene.Node.to_global_id('DepartmentNode', department.id)
            site_structure.append({'url': f'/{department.slug}/', 'type': 'department', 'id': department_global_id})

        site_structure.extend(get_structure_for_content_type('service page'))
        site_structure.extend(get_structure_for_content_type('information page'))
        site_structure.extend(get_structure_for_content_type('official document page'))
        site_structure.extend(get_structure_for_content_type('guide page'))
        site_structure.extend(get_structure_for_content_type('form container'))
        site_structure.extend(get_structure_for_content_type('location page'))
        site_structure.extend(get_structure_for_content_type('event page'))

        return site_structure


class InformationPageContactNode(DjangoObjectType):
    class Meta:
        model = InformationPageContact
        interfaces = [graphene.Node]


class InformationPageTopicNode(DjangoObjectType):
    class Meta:
        model = InformationPageTopic
        interfaces = [graphene.Node]
        filter_fields = ['topic']


class FormContainerTopicNode(DjangoObjectType):
    class Meta:
        model = FormContainerTopic
        interfaces = [graphene.Node]
        filter_fields = ['topic']


class DepartmentPageContactNode(DjangoObjectType):
    class Meta:
        model = DepartmentPageContact
        interfaces = [graphene.Node]


class DepartmentPageDirectorNode(DjangoObjectType):
    class Meta:
        model = DepartmentPageDirector
        interfaces = [graphene.Node]

# Get the original page object from a page chooser node
# Works for any content_type defined in content_type_map


def get_page_from_content_type(self):
    content_type = self.page.content_type.name
    model = content_type_map[content_type]["model"]
    page = model.objects.get(id=self.page_id)
    return page

# Get a page global_id from a page chooser node
# Works for any content_type defined in content_type_map


def get_global_id_from_content_type(self):
    content_type = self.page.content_type.name
    node = content_type_map[content_type]["node"]
    global_id = graphene.Node.to_global_id(node, self.page_id)
    return global_id


class DepartmentPageTopPageNode(DjangoObjectType):
    title = graphene.String()
    slug = graphene.String()
    page_id = graphene.ID()

    def resolve_page_id(self, info):
        return get_global_id_from_content_type(self)

    def resolve_title(self, resolve_info, *args, **kwargs):
        return get_page_from_content_type(self).title

    def resolve_slug(self, resolve_info, *args, **kwargs):
        return get_page_from_content_type(self).slug

    class Meta:
        model = DepartmentPageTopPage
        interfaces = [graphene.Node]


class DepartmentPageRelatedPageNode(DjangoObjectType):
    title = graphene.String()
    slug = graphene.String()
    page_id = graphene.ID()

    def resolve_page_id(self, info):
        return get_global_id_from_content_type(self)

    def resolve_title(self, resolve_info, *args, **kwargs):
        return get_page_from_content_type(self).title

    def resolve_slug(self, resolve_info, *args, **kwargs):
        return get_page_from_content_type(self).slug

    class Meta:
        model = DepartmentPageRelatedPage
        interfaces = [graphene.Node]


class TopicPageTopPageNode(DjangoObjectType):
    title = graphene.String()
    slug = graphene.String()
    page_id = graphene.ID()
    page_type = graphene.String()

    def resolve_page_id(self, info):
        return get_global_id_from_content_type(self)

    def resolve_title(self, resolve_info, *args, **kwargs):
        return get_page_from_content_type(self).title

    def resolve_slug(self, resolve_info, *args, **kwargs):
        return get_page_from_content_type(self).slug

    def resolve_page_type(self, info):
        return self.page.content_type.name

    class Meta:
        model = TopicPageTopPage
        interfaces = [graphene.Node]


class OfficialDocumentPageTopicNode(DjangoObjectType):
    class Meta:
        model = OfficialDocumentPageTopic
        interfaces = [graphene.Node]
        filter_fields = ['topic']


class GuidePageTopicNode(DjangoObjectType):
    class Meta:
        model = GuidePageTopic
        interfaces = [graphene.Node]
        filter_fields = ['topic']


def get_page_with_preview_data(page, session):
    # Wagtail saves preview data in the session. We want to mimick what they're doing to generate the built-in preview.
    # https://github.com/wagtail/wagtail/blob/db6d36845f3f2c5d7009a22421c2efab9968aa24/wagtail/admin/views/pages.py#L544
    # TODO: This should be simpler. Instead of hijacking the wagtail admin, it'd probably be easier to create a new endpoint
    #       or have a graphql mutation do the work
    session_key = f'wagtail-preview-{page.pk}'
    preview_data, timestamp = session.get(session_key, [None, None])
    if not preview_data:
        return None

    preview_data = {key: vals[0] for key, vals in preview_data.items()}
    parent = page.get_parent().specific
    FormKlass = page.get_edit_handler().get_form_class(page._meta.model)

    form = FormKlass(preview_data, instance=page, parent_page=parent)
    if not form.is_valid():
        raise Exception(form.errors.as_json())
    obj = form.save(commit=False)

    return obj


class Query(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')

    department_page = graphene.Node.Field(DepartmentPageNode)
    all_service_pages = DjangoFilterConnectionField(ServicePageNode)
    page_revision = graphene.Field(PageRevisionNode, id=graphene.ID())
    site_structure = graphene.Field(SiteStructure)
    all_page_revisions = DjangoFilterConnectionField(PageRevisionNode)
    all_information_pages = DjangoFilterConnectionField(InformationPageNode)
    all_department_pages = DjangoFilterConnectionField(DepartmentPageNode)
    all_themes = DjangoFilterConnectionField(ThemeNode)
    all_topics = DjangoFilterConnectionField(TopicNode)
    all_topic_collections = DjangoFilterConnectionField(TopicCollectionNode)
    all_departments = DjangoFilterConnectionField(DepartmentNode)
    all_official_document_pages = DjangoFilterConnectionField(
        OfficialDocumentPageNode)
    all_guide_pages = DjangoFilterConnectionField(GuidePageNode)
    all_form_containers = DjangoFilterConnectionField(FormContainerNode)
    all_topic_page_topic_collections = DjangoFilterConnectionField(TopicPageTopicCollectionNode)
    all_service_page_topics = DjangoFilterConnectionField(ServicePageTopicNode)
    all_information_page_topics = DjangoFilterConnectionField(InformationPageTopicNode)
    all_official_document_page_topics = DjangoFilterConnectionField(OfficialDocumentPageTopicNode)
    all_guide_page_topics = DjangoFilterConnectionField(GuidePageTopicNode)
    all_location_pages = DjangoFilterConnectionField(LocationPageNode)
    all_form_container_topics = DjangoFilterConnectionField(FormContainerTopicNode)
    all_event_pages = DjangoFilterConnectionField(EventPageNode)
    all_ordered_events = DjangoFilterConnectionField(EventPageNode, filterset_class=EventFilter)

    def resolve_site_structure(self, resolve_info):
        site_structure = SiteStructure()
        return site_structure

    def resolve_page_revision(self, resolve_info, id=None):
        revision = graphene.Node.get_node_from_global_id(resolve_info, id)
        return revision


schema = graphene.Schema(query=Query)

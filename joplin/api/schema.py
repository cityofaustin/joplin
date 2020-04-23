import django.utils.translation
import graphene
from django.core.exceptions import ObjectDoesNotExist
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField
from graphene.types import Scalar
from graphene.types.generic import GenericScalar
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import PageRevision
from django_filters import FilterSet, OrderingFilter
from wagtail.documents.models import Document
from wagtail.core.rich_text import expand_db_html
import graphql_jwt
from graphql_jwt.decorators import superuser_required

from snippets.contact.models import Contact, ContactPhoneNumber
from snippets.theme.models import Theme
from base.models import TranslatedImage
from pages.topic_collection_page.models import TopicCollectionPage, JanisBasePageWithTopicCollections, JanisBasePageTopicCollection
from pages.topic_page.models import TopicPage, TopicPageTopPage, JanisBasePageWithTopics, JanisBasePageTopic
from pages.service_page.models import ServicePage
from pages.information_page.models import InformationPage
from pages.department_page.models import DepartmentPage, DepartmentPageDirector, DepartmentPageTopPage, DepartmentPageRelatedPage
from pages.official_documents_page.models import OfficialDocumentPage, OfficialDocumentPageDocument
from pages.guide_page.models import GuidePage
from pages.form_container.models import FormContainer
from pages.base_page.models import JanisBasePage
from .content_type_map import content_type_map
import traceback
from pages.location_page.models import LocationPage, LocationPageRelatedServices
from pages.event_page.models import EventPage, EventPageFee
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
        dict_values = {key: try_expand_db_html(value) for (key, value) in item.items() if
                       item is not isinstance(item, int)}
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


class ContextualNavInstance(graphene.ObjectType):
    id = graphene.String()
    url = graphene.String()
    title = graphene.String()


class ContextualNavData(graphene.ObjectType):
    url = graphene.String()
    parent = graphene.Field(ContextualNavInstance)
    grandparent = graphene.Field(ContextualNavInstance)
    # TODO: determine if this is possible in a later issue
    # related_to = graphene.List(JanisBasePageTopicCollectionNode)


class JanisBasePageNode(DjangoObjectType):
    janis_urls = graphene.List(graphene.String)
    janis_instances = graphene.List(ContextualNavData)
    page_type = graphene.String()
    summery = graphene.String()

    class Meta:
        model = JanisBasePage
        filter_fields = ['id', 'slug', 'live']
        interfaces = [graphene.Node]

    def resolve_janis_urls(self, info):
        return self.specific.janis_urls()

    def resolve_page_type(self, info):
        return self.content_type

    def resolve_summery(self, info):
        if hasattr(self.specific, "short_description"):
            return self.specific.short_description
        elif hasattr(self.specific, "mission"):
            return self.specific.mission

    def resolve_janis_instances(self, info):
        instances = []
        for i in self.specific.janis_instances():
            if i['url']:
                url = i['url']
            else:
                url = ''
            if i['parent']:
                node = content_type_map[i['parent'].content_type.name]["node"]
                global_id = graphene.Node.to_global_id(node, i['parent'].id)
                parent = ContextualNavInstance(
                    id=global_id,
                    title=i['parent'].title,
                    url=i['parent'].specific.janis_urls()[0])
            else:
                parent = None
            if i['grandparent']:
                node = content_type_map[i['grandparent'].content_type.name]["node"]
                global_id = graphene.Node.to_global_id(node, i['grandparent'].id)
                grandparent = ContextualNavInstance(
                    id=global_id,
                    title=i['grandparent'].title,
                    url=i['grandparent'].specific.janis_urls()[0])
            else:
                grandparent = None
            instance = ContextualNavData(parent=parent, grandparent=grandparent, url=url)
            instances.append(instance)
        return instances


class JanisBasePageWithTopicCollectionsNode(DjangoObjectType):
    class Meta:
        model = JanisBasePageWithTopicCollections
        filter_fields = ['id', 'slug', 'live']
        interfaces = [graphene.Node]


'''
    Note: we do NOT want to use DjangoObjectType for the User model.
    Otherwise owners and users will be visible on all nodes by default.
    We want Nodes to be explicit if they want to resolve users,
    and we want those resolvers to be wrapped in a @superuser_required decorator for authorization.
    TODO: handle importing of department groups for non-superusers.
'''


class OwnerNode(graphene.ObjectType):
    id = graphene.ID()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    is_superuser = graphene.String()

    @superuser_required
    def resolve_id(self, info):
        return self.id

    @superuser_required
    def resolve_first_name(self, info):
        return self.first_name

    @superuser_required
    def resolve_last_name(self, info):
        return self.last_name

    @superuser_required
    def resolve_email(self, info):
        return self.email

    @superuser_required
    def resolve_is_superuser(self, info):
        return self.is_superuser


# Add this method to a PageNode to allow authorized users to see page owner data.
def resolve_owner_handler(self, info):
    owner = self.owner
    if owner:
        return OwnerNode(
            id=owner.id,
            first_name=owner.first_name,
            last_name=owner.last_name,
            email=owner.email,
            is_superuser=owner.is_superuser,
        )


class DepartmentPageNode(DjangoObjectType):
    page_type = graphene.String()
    owner = graphene.Field(OwnerNode)

    class Meta:
        model = DepartmentPage
        filter_fields = ['id', 'slug', 'live']
        interfaces = [graphene.Node]

    def resolve_page_type(self, info):
        return DepartmentPage.get_verbose_name().lower()

    @superuser_required
    def resolve_owner(self, info):
        return resolve_owner_handler(self, info)


class DepartmentResolver(graphene.Interface):
    departments = graphene.List(DepartmentPageNode)

    @classmethod
    def resolve_departments(cls, instance, info):
        return instance.departments()


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
    owner = graphene.Field(OwnerNode)

    class Meta:
        model = TopicCollectionPage
        filter_fields = ['id', 'slug', 'live']
        interfaces = [graphene.Node]

    @superuser_required
    def resolve_owner(self, info):
        return resolve_owner_handler(self, info)


class JanisBasePageTopicCollectionNode(DjangoObjectType):
    class Meta:
        model = JanisBasePageTopicCollection
        filter_fields = ['topic_collection']
        fields = '__all__'
        interfaces = [graphene.Node]


class TopicNode(DjangoObjectType):
    topiccollections = graphene.List(TopicCollectionNode)
    owner = graphene.Field(OwnerNode)

    class Meta:
        model = TopicPage
        filter_fields = ['id', 'slug', 'live']
        interfaces = [graphene.Node]

    def resolve_topiccollections(self, info):
        tc = []
        for t in self.topic_collections.values():
            tc.append(TopicCollectionPage.objects.get(id=t['topic_collection_id']))
        return tc

    @superuser_required
    def resolve_owner(self, info):
        return resolve_owner_handler(self, info)


class JanisBasePageTopicNode(DjangoObjectType):
    page_id = graphene.ID()

    class Meta:
        model = JanisBasePageTopic
        filter_fields = ['topic']
        fields = '__all__'
        interfaces = [graphene.Node]

    def resolve_page_id(self, info):
        return get_global_id_from_content_type(self)


class JanisBasePageWithTopicsNode(DjangoObjectType):
    departments = graphene.List(DepartmentPageNode)
    topics = graphene.List(TopicNode)

    class Meta:
        model = JanisBasePageWithTopics
        filter_fields = ['id', 'slug', 'live']
        interfaces = [graphene.Node]

    def resolve_topics(self, info):
        topics = []
        for topic in self.topics.values():
            topics.append(TopicPage.objects.get(id=topic['topic_id']))
        return topics

    def resolve_departments(self, info):
        return self.departments()


class LocationPageNode(DjangoObjectType):
    page_type = graphene.String()
    janis_urls = graphene.List(graphene.String)
    owner = graphene.Field(OwnerNode)

    class Meta:
        model = LocationPage
        filter_fields = ['id', 'slug', 'live']
        fields = '__all__'
        interfaces = [graphene.Node, DepartmentResolver]

    @superuser_required
    def resolve_owner(self, info):
        return resolve_owner_handler(self, info)

    def resolve_page_type(self, info):
        return LocationPage.get_verbose_name().lower()

    def resolve_janis_urls(self, info):
        return self.janis_urls()


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

    # For reference:
    # https://django-filter.readthedocs.io/en/master/ref/filterset.html#declaring-filterable-fields
    # https://docs.djangoproject.com/en/3.0/ref/models/querysets/#lte

    class Meta:
        model = EventPage
        fields = {
            'date': ['exact', 'lte', 'gte'],
            'live': ['exact'],
            'id': ['exact'],
            'canceled': ['exact'],
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
    page_type = graphene.String()
    janis_urls = graphene.List(graphene.String)
    owner = graphene.Field(OwnerNode)

    class Meta:
        model = EventPage
        filter_fields = ['id', 'slug', 'live', 'date']
        interfaces = [graphene.Node, DepartmentResolver]

    def resolve_locations(self, info):
        repr_locations = []
        for block in self.location_blocks.stream_data:
            value = block.get('value')
            location_type = block.get('type')
            repr_locations.append(EventPageLocation(value=value, location_type=location_type))

        return repr_locations

    @superuser_required
    def resolve_owner(self, info):
        return resolve_owner_handler(self, info)

    def resolve_page_type(self, info):
        return EventPage.get_verbose_name().lower()

    def resolve_janis_urls(self, info):
        return self.janis_urls()


class EventPageFeeNode(DjangoObjectType):
    class Meta:
        model = EventPageFee
        interfaces = [graphene.Node]


class ContactNode(DjangoObjectType):
    class Meta:
        model = Contact
        interfaces = [graphene.Node]


class ContactPhoneNumberNode(DjangoObjectType):
    class Meta:
        model = ContactPhoneNumber
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
    janis_url = graphene.List(graphene.String)
    owner = graphene.Field(OwnerNode)

    class Meta:
        model = ServicePage
        filter_fields = ['id', 'slug', 'live', 'coa_global']
        interfaces = [graphene.Node, DepartmentResolver]

    def resolve_page_type(self, info):
        return ServicePage.get_verbose_name().lower()

    def resolve_janis_url(self, info):
        return self.janis_urls()

    @superuser_required
    def resolve_owner(self, info):
        return resolve_owner_handler(self, info)


class InformationPageNode(DjangoObjectType):
    page_type = graphene.String()
    owner = graphene.Field(OwnerNode)

    class Meta:
        model = InformationPage
        filter_fields = ['id', 'slug', 'live', 'coa_global']
        interfaces = [graphene.Node, DepartmentResolver]

    def resolve_page_type(self, info):
        return InformationPage.get_verbose_name().lower()

    @superuser_required
    def resolve_owner(self, info):
        return resolve_owner_handler(self, info)


class FormContainerNode(DjangoObjectType):
    page_type = graphene.String()
    owner = graphene.Field(OwnerNode)

    class Meta:
        model = FormContainer
        filter_fields = ['id', 'slug', 'live', 'coa_global']
        interfaces = [graphene.Node, DepartmentResolver]

    def resolve_page_type(self, info):
        return FormContainer.get_verbose_name().lower()

    @superuser_required
    def resolve_owner(self, info):
        return resolve_owner_handler(self, info)


class OfficialDocumentFilter(FilterSet):
    order_by = OrderingFilter(
        fields=(
            ('date'),
        )
    )

    class Meta:
        model = OfficialDocumentPageDocument
        fields = ['date']


class DocumentNodeDocument(graphene.ObjectType):
    filename = graphene.String()
    fileSize = graphene.String()


class OfficialDocumentPageDocumentNode(DjangoObjectType):
    document = graphene.Field(DocumentNodeDocument)

    class Meta:
        model = OfficialDocumentPageDocument
        filter_fields = ['date']
        interfaces = [graphene.Node]

    def resolve_document(self, info):
        english_doc = DocumentNodeDocument(
            filename=self.document.filename,
            fileSize=self.document.file_size,
        )
        if django.utils.translation.get_language() == 'es':
            if self.document_es:
                return DocumentNodeDocument(
                    filename=self.document_es.filename,
                    fileSize=self.document_es.file_size,
                )
            else:
                return english_doc
        else:
            return english_doc


class OfficialDocumentPageNode(DjangoObjectType):
    page_type = graphene.String()
    official_documents = DjangoFilterConnectionField(
        OfficialDocumentPageDocumentNode, filterset_class=OfficialDocumentFilter)
    owner = graphene.Field(OwnerNode)

    class Meta:
        model = OfficialDocumentPage
        filter_fields = ['id', 'slug', 'live', 'coa_global']
        interfaces = [graphene.Node, DepartmentResolver]

    def resolve_page_type(self, info):
        return OfficialDocumentPage.get_verbose_name().lower()

    @superuser_required
    def resolve_owner(self, info):
        return resolve_owner_handler(self, info)


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
            return page.janis_publish_url()
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
    owner = graphene.Field(OwnerNode)

    class Meta:
        model = GuidePage
        filter_fields = ['id', 'slug', 'live', 'coa_global']
        interfaces = [graphene.Node, DepartmentResolver]

    def resolve_sections(self, info):
        repr_sections = []
        for block in self.sections.stream_data:
            value = block.get('value')
            repr_sections.append(GuidePageSection(value=value))

        return repr_sections

    def resolve_page_type(self, info):
        return GuidePage.get_verbose_name().lower()

    @superuser_required
    def resolve_owner(self, info):
        return resolve_owner_handler(self, info)


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
    preview_janis_instance = graphene.NonNull(ContextualNavData)
    is_latest = graphene.Boolean()
    is_live = graphene.Boolean()
    page_type = graphene.String()

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

    def resolve_is_latest(self, resolve_info, *args, **kwargs):
        return self.created_at == self.page.latest_revision_created_at

    def resolve_is_live(self, resolve_info, *args, **kwargs):
        return self == self.page.live_revision

    def resolve_page_type(self, resolve_info, *args, **kwargs):
        return self.page.content_type.name

    def resolve_preview_janis_instance(self, resolve_info, *args, **kwargs):
        preview_instance = {}

        # for now just get the first one
        page = self.as_page_object()
        instances = page.janis_instances()
        if instances and instances[0]:
            preview_instance = instances[0]

        return preview_instance

    class Meta:
        model = PageRevision
        filter_fields = ['id']
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


# Allow users to request JWT token for authorization-protected resolvers
# https://django-graphql-jwt.domake.io/en/latest/quickstart.html
class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')

    all_pages = DjangoFilterConnectionField(JanisBasePageNode)

    department_page = graphene.Node.Field(DepartmentPageNode)
    all_service_pages = DjangoFilterConnectionField(ServicePageNode)
    page_revision = graphene.Field(PageRevisionNode, id=graphene.ID())
    all_page_revisions = DjangoFilterConnectionField(PageRevisionNode)
    all_information_pages = DjangoFilterConnectionField(InformationPageNode)
    all_department_pages = DjangoFilterConnectionField(DepartmentPageNode)
    all_themes = DjangoFilterConnectionField(ThemeNode)
    all_topics = DjangoFilterConnectionField(TopicNode)
    all_topic_collections = DjangoFilterConnectionField(TopicCollectionNode)
    all_official_document_pages = DjangoFilterConnectionField(
        OfficialDocumentPageNode)
    all_guide_pages = DjangoFilterConnectionField(GuidePageNode)
    all_form_containers = DjangoFilterConnectionField(FormContainerNode)
    all_location_pages = DjangoFilterConnectionField(LocationPageNode)
    all_event_pages = DjangoFilterConnectionField(EventPageNode, filterset_class=EventFilter)
    topic_collection_topics = DjangoFilterConnectionField(JanisBasePageTopicCollectionNode)
    base_page_topics = DjangoFilterConnectionField(JanisBasePageTopicNode)

    def resolve_page_revision(self, resolve_info, id=None):
        revision = graphene.Node.get_node_from_global_id(resolve_info, id)
        return revision


schema = graphene.Schema(query=Query, mutation=Mutation)

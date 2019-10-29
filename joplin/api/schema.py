import django.utils.translation
import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField
from graphene.types import Scalar
from graphene.types.json import JSONString
from graphene.types.generic import GenericScalar
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page, PageRevision
from django_filters import FilterSet, OrderingFilter
from wagtail.core.blocks import *
from wagtail.documents.models import Document
from wagtail.core.rich_text import expand_db_html
from base.models import JanisBasePage, TranslatedImage, ThreeOneOne, ServicePage, ServicePageContact, ServicePageTopic, ServicePageRelatedDepartments, InformationPageRelatedDepartments, ProcessPage, ProcessPageStep, ProcessPageContact, ProcessPageTopic, InformationPage, InformationPageContact, InformationPageTopic, DepartmentPage, DepartmentPageContact, DepartmentPageDirector, Theme, TopicCollectionPage, TopicPage, Contact, Location, ContactDayAndDuration, Department, DepartmentContact, TopicPageTopicCollection, OfficialDocumentPage, OfficialDocumentPageRelatedDepartments, OfficialDocumentPageTopic, OfficialDocumentPageOfficialDocument, GuidePage, GuidePageTopic, GuidePageRelatedDepartments, GuidePageContact, JanisBasePage, PhoneNumber, DepartmentPageTopPage, DepartmentPageRelatedPage, TopicPageTopPage, FormPage, FormPageRelatedDepartments, FormPageTopic
import traceback
import pdb

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
        print('Streamfield API Exception!', e)
        print(traceback.format_exc())
        return parsed_item


def expand_dict_values(item):
    """
    dict comprehension that expands db html on each item in a dict
    """
    return {key: try_expand_db_html(value) for (key, value) in item.items()}


def expand_by_type(key, value):
    """
    recursive function to
    handle the streamfield black items differently depending on type
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
    try:
        block = StreamChild.block.get_api_representation(StreamChild.value)
        # if the block is just a string (no dict at all), just return it expanded
        if isinstance(block, str):
            parsed_block = try_expand_db_html(block)
            return parsed_block
        else:
            parsed_block = {key: expand_by_type(key, value) for (key, value) in block.items()}

        return parsed_block
    except Exception as e:
        print('Streamfield API Exception!', e)
        print(traceback.format_exc())
        return block


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


class ThreeOneOneNode(DjangoObjectType):
    class Meta:
        model = ThreeOneOne
        filter_fields = ['title']
        interfaces = [graphene.Node]


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


class FormPageRelatedDepartmentsNode(DjangoObjectType):
    class Meta:
        model = FormPageRelatedDepartments
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
    class Meta:
        model = ServicePage
        filter_fields = ['id', 'slug', 'live', 'coa_global']
        interfaces = [graphene.Node]


class InformationPageNode(DjangoObjectType):
    class Meta:
        model = InformationPage
        filter_fields = ['id', 'slug', 'live', 'coa_global']
        interfaces = [graphene.Node]


class DepartmentPageNode(DjangoObjectType):
    class Meta:
        model = DepartmentPage
        filter_fields = ['id', 'slug', 'live']
        interfaces = [graphene.Node]


class FormPageNode(DjangoObjectType):
    class Meta:
        model = FormPage
        filter_fields = ['id', 'slug', 'live', 'coa_global']
        interfaces = [graphene.Node]


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
    official_documents = DjangoFilterConnectionField(
        OfficialDocumentPageOfficialDocumentNode, filterset_class=OfficialDocumentFilter)

    class Meta:
        model = OfficialDocumentPage
        filter_fields = ['id', 'slug', 'live', 'coa_global']
        interfaces = [graphene.Node]


class GuidePageSectionPageBlock(graphene.ObjectType):
    # This uses graphene ObjectType resolvers, see:
    # https://docs.graphene-python.org/en/latest/types/objecttypes/#resolvers

    value = GenericScalar()
    service_page = graphene.Field(ServicePageNode)
    information_page = graphene.Field(InformationPageNode)
    url = graphene.String()

    def resolve_url(self, resolve_info, *args, **kwargs):
        page = None
        try:
            page = ServicePage.objects.get(id=self.value)
        except Exception as e:
            try:
                page = InformationPage.objects.get(id=self.value)
            except Exception as e:
                pass
            pass

        if page:
            return page.janis_url()
        else:
            return '#'

    def resolve_service_page(self, info):
        service_page = None
        # TODO: don't catch everything
        try:
            service_page = ServicePage.objects.get(id=self.value)
        except Exception as e:
            pass

        return service_page

    def resolve_information_page(self, info):
        information_page = None
        # TODO: don't catch everything
        try:
            information_page = InformationPage.objects.get(id=self.value)
        except Exception as e:
            pass

        return information_page


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


class PageRevisionNode(DjangoObjectType):
    as_service_page = graphene.NonNull(ServicePageNode)
    as_information_page = graphene.NonNull(InformationPageNode)
    as_department_page = graphene.NonNull(DepartmentPageNode)
    as_topic_page = graphene.NonNull(TopicNode)
    as_topic_collection_page = graphene.NonNull(TopicCollectionNode)
    as_official_document_page = graphene.NonNull(OfficialDocumentPageNode)
    as_guide_page = graphene.NonNull(GuidePageNode)
    as_form_page = graphene.NonNull(FormPageNode)

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

    def resolve_as_form_page(self, resolve_info, *args, **kwargs):
        return self.as_page_object()

    class Meta:
        model = PageRevision
        filter_fields = ['id']
        interfaces = [graphene.Node]

def get_structure_for_content_type(content_type):
    content_type_map = {
        "service page": {
            "node": "DepartmentNode",
            "model": ServicePage,
        },
        "information page": {
            "node": "InformationPageNode",
            "model": InformationPage,
        },
        "official document page": {
            "node": "OfficialDocumentPageNode",
            "model": OfficialDocumentPage,
        },
        "guide page": {
            "node": "GuidePageNode",
            "model": GuidePage,
        },
        "form page": {
            "node": "FormPageNode",
            "model": FormPage,
        },
    }
    site_structure = []
    content_type_data = content_type_map.get(content_type, None)
    if not content_type_data:
        raise Exception(f'content_type [{content_type}] is not included in content_type_map')

    pages = content_type_data["model"].objects.all()
    for page in pages:
        page_global_id = graphene.Node.to_global_id(content_type_data["node"], page.id)

        if page.coa_global:
            site_structure.append({'url' :f'/{page.slug}/', 'type': content_type, 'id': page_global_id})

        if page.get("related_departments", None):
            page_departments = page.related_departments.all()
            for page_department in page_departments:
                page_department_global_id = graphene.Node.to_global_id('DepartmentNode', page_department.related_department.id)
                site_structure.append({'url' :f'/{page_department.related_department.slug}/{page.slug}/', 'type': content_type, 'id': page_global_id, 'parent_department': page_department_global_id})

        if page.get("topics", None):
            page_topics = page.topics.all()
            for page_topic in page_topics:
                page_topic_global_id = graphene.Node.to_global_id('TopicNode', page_topic.topic.id)
                page_topic_tcs = page_topic.topic.topiccollections.all()
                for tc in information_page_topic_tcs:
                    if not tc.topiccollection.theme:
                        continue

                    page_topic_tc_global_id = graphene.Node.to_global_id('TopicCollectionNode', tc.topiccollection.id)
                    site_structure.append({'url' :f'/{tc.topiccollection.theme.slug}/{tc.topiccollection.slug}/{page_topic.topic.slug}/{page.slug}/', 'type': content_type, 'id': page_global_id, 'parent_topic': page_topic_global_id, 'grandparent_topic_collection': page_topic_tc_global_id})
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
            site_structure.append({'url' :f'/{topic_collection.theme.slug}/{topic_collection.slug}/', 'type': 'topic collection', 'id': topic_collection_global_id});

        topics = TopicPage.objects.all()
        for topic in topics:
            topic_global_id = graphene.Node.to_global_id('TopicNode', topic.id)
            topic_tcs = topic.topiccollections.all()
            for tc in topic_tcs:
                if not tc.topiccollection.theme:
                    continue

                topic_tc_global_id = graphene.Node.to_global_id('TopicCollectionNode', tc.topiccollection.id)
                site_structure.append({'url' :f'/{tc.topiccollection.theme.slug}/{tc.topiccollection.slug}/{topic.slug}/', 'type': 'topic', 'id': topic_global_id, 'parent_topic_collection': topic_tc_global_id})

        departments = DepartmentPage.objects.all()
        for department in departments:
            department_global_id = graphene.Node.to_global_id('DepartmentNode', department.id)
            site_structure.append({'url' :f'/{department.slug}/', 'type': 'department', 'id': department_global_id})

        site_structure.extend(get_structure_for_content_type('service page'))
        site_structure.extend(get_structure_for_content_type('information page'))
        site_structure.extend(get_structure_for_content_type('official document page'))
        site_structure.extend(get_structure_for_content_type('guide page'))
        site_structure.extend(get_structure_for_content_type('form page'))

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


class FormPageTopicNode(DjangoObjectType):
    class Meta:
        model = FormPageTopic
        interfaces = [graphene.Node]


class DepartmentPageContactNode(DjangoObjectType):
    class Meta:
        model = DepartmentPageContact
        interfaces = [graphene.Node]


class DepartmentPageDirectorNode(DjangoObjectType):
    class Meta:
        model = DepartmentPageDirector
        interfaces = [graphene.Node]


class DepartmentPageTopPageNode(DjangoObjectType):
    title = graphene.String()
    slug = graphene.String()
    page_id = graphene.ID()

    def resolve_page_id(self, info):
        # TODO: don't catch everything
        try:
            service_page_global_id = graphene.Node.to_global_id('ServicePageNode', self.page_id)
            return service_page_global_id
        except Exception as e:
            pass

        # TODO: don't catch everything
        try:
            information_page_global_id = graphene.Node.to_global_id('InformationPageNode', self.page_id)
            return information_page_global_id
        except Exception as e:
            pass

        # TODO: don't catch everything
        try:
            guide_page_global_id = graphene.Node.to_global_id('GuidePageNode', self.page_id)
            return guide_page_global_id
        except Exception as e:
            pass

        # TODO: don't catch everything
        try:
            official_document_page_global_id = graphene.Node.to_global_id('OfficialDocumentPageNode', self.page_id)
            return official_document_page_global_id
        except Exception as e:
            pass


    def resolve_title(self, resolve_info, *args, **kwargs):
        service_page = None
        # TODO: don't catch everything
        try:
            service_page = ServicePage.objects.get(id=self.page_id)
            return service_page.title
        except Exception as e:
            pass

        information_page = None
        # TODO: don't catch everything
        try:
            information_page = InformationPage.objects.get(id=self.page_id)
            return information_page.title
        except Exception as e:
            pass

        guide_page = None
        # TODO: don't catch everything
        try:
            guide_page = GuidePage.objects.get(id=self.page_id)
            return guide_page.title
        except Exception as e:
            pass

        official_document_page = None
        # TODO: don't catch everything
        try:
            official_document_page = OfficialDocumentPage.objects.get(id=self.page_id)
            return official_document_page.title
        except Exception as e:
            pass

    def resolve_slug(self, resolve_info, *args, **kwargs):
        service_page = None
        # TODO: don't catch everything
        try:
            service_page = ServicePage.objects.get(id=self.page_id)
            return service_page.slug
        except Exception as e:
            pass

        information_page = None
        # TODO: don't catch everything
        try:
            information_page = InformationPage.objects.get(id=self.page_id)
            return information_page.slug
        except Exception as e:
            pass

        guide_page = None
        # TODO: don't catch everything
        try:
            guide_page = GuidePage.objects.get(id=self.page_id)
            return guide_page.slug
        except Exception as e:
            pass

        official_document_page = None
        # TODO: don't catch everything
        try:
            official_document_page = OfficialDocumentPage.objects.get(id=self.page_id)
            return official_document_page.slug
        except Exception as e:
            pass

    def resolve_form_page(self, info):
        form_page = None
        # TODO: don't catch everything
        try:
            form_page = FormPage.objects.get(id=self.page_id)
        except Exception as e:
            pass

        return form_page

    class Meta:
        model = DepartmentPageTopPage
        interfaces = [graphene.Node]


class DepartmentPageRelatedPageNode(DjangoObjectType):
    title = graphene.String()
    slug = graphene.String()
    page_id = graphene.ID()

    def resolve_page_id(self, info):
        # TODO: don't catch everything
        try:
            service_page_global_id = graphene.Node.to_global_id('ServicePageNode', self.page_id)
            return service_page_global_id
        except Exception as e:
            pass

        # TODO: don't catch everything
        try:
            information_page_global_id = graphene.Node.to_global_id('InformationPageNode', self.page_id)
            return information_page_global_id
        except Exception as e:
            pass

        # TODO: don't catch everything
        try:
            guide_page_global_id = graphene.Node.to_global_id('GuidePageNode', self.page_id)
            return guide_page_global_id
        except Exception as e:
            pass

        # TODO: don't catch everything
        try:
            official_document_page_global_id = graphene.Node.to_global_id('OfficialDocumentPageNode', self.page_id)
            return official_document_page_global_id
        except Exception as e:
            pass


    def resolve_title(self, resolve_info, *args, **kwargs):
        service_page = None
        # TODO: don't catch everything
        try:
            service_page = ServicePage.objects.get(id=self.page_id)
            return service_page.title
        except Exception as e:
            pass

        information_page = None
        # TODO: don't catch everything
        try:
            information_page = InformationPage.objects.get(id=self.page_id)
            return information_page.title
        except Exception as e:
            pass

        guide_page = None
        # TODO: don't catch everything
        try:
            guide_page = GuidePage.objects.get(id=self.page_id)
            return guide_page.title
        except Exception as e:
            pass

        official_document_page = None
        # TODO: don't catch everything
        try:
            official_document_page = OfficialDocumentPage.objects.get(id=self.page_id)
            return official_document_page.title
        except Exception as e:
            pass

    def resolve_slug(self, resolve_info, *args, **kwargs):
        service_page = None
        # TODO: don't catch everything
        try:
            service_page = ServicePage.objects.get(id=self.page_id)
            return service_page.slug
        except Exception as e:
            pass

        information_page = None
        # TODO: don't catch everything
        try:
            information_page = InformationPage.objects.get(id=self.page_id)
            return information_page.slug
        except Exception as e:
            pass

        guide_page = None
        # TODO: don't catch everything
        try:
            guide_page = GuidePage.objects.get(id=self.page_id)
            return guide_page.slug
        except Exception as e:
            pass

        official_document_page = None
        # TODO: don't catch everything
        try:
            official_document_page = OfficialDocumentPage.objects.get(id=self.page_id)
            return official_document_page.slug
        except Exception as e:
            pass

    class Meta:
        model = DepartmentPageRelatedPage
        interfaces = [graphene.Node]


class TopicPageTopPageNode(DjangoObjectType):
    title = graphene.String()
    slug = graphene.String()
    page_id = graphene.ID()

    def resolve_page_id(self, info):
        # TODO: don't catch everything
        try:
            service_page_global_id = graphene.Node.to_global_id('ServicePageNode', self.page_id)
            return service_page_global_id
        except Exception as e:
            pass

        # TODO: don't catch everything
        try:
            information_page_global_id = graphene.Node.to_global_id('InformationPageNode', self.page_id)
            return information_page_global_id
        except Exception as e:
            pass

        # TODO: don't catch everything
        try:
            guide_page_global_id = graphene.Node.to_global_id('GuidePageNode', self.page_id)
            return guide_page_global_id
        except Exception as e:
            pass

        # TODO: don't catch everything
        try:
            official_document_page_global_id = graphene.Node.to_global_id('OfficialDocumentPageNode', self.page_id)
            return official_document_page_global_id
        except Exception as e:
            pass


    def resolve_title(self, resolve_info, *args, **kwargs):
        service_page = None
        # TODO: don't catch everything
        try:
            service_page = ServicePage.objects.get(id=self.page_id)
            return service_page.title
        except Exception as e:
            pass

        information_page = None
        # TODO: don't catch everything
        try:
            information_page = InformationPage.objects.get(id=self.page_id)
            return information_page.title
        except Exception as e:
            pass

        guide_page = None
        # TODO: don't catch everything
        try:
            guide_page = GuidePage.objects.get(id=self.page_id)
            return guide_page.title
        except Exception as e:
            pass

        official_document_page = None
        # TODO: don't catch everything
        try:
            official_document_page = OfficialDocumentPage.objects.get(id=self.page_id)
            return official_document_page.title
        except Exception as e:
            pass

    def resolve_slug(self, resolve_info, *args, **kwargs):
        service_page = None
        # TODO: don't catch everything
        try:
            service_page = ServicePage.objects.get(id=self.page_id)
            return service_page.slug
        except Exception as e:
            pass

        information_page = None
        # TODO: don't catch everything
        try:
            information_page = InformationPage.objects.get(id=self.page_id)
            return information_page.slug
        except Exception as e:
            pass

        guide_page = None
        # TODO: don't catch everything
        try:
            guide_page = GuidePage.objects.get(id=self.page_id)
            return guide_page.slug
        except Exception as e:
            pass

        official_document_page = None
        # TODO: don't catch everything
        try:
            official_document_page = OfficialDocumentPage.objects.get(id=self.page_id)
            return official_document_page.slug
        except Exception as e:
            pass

    def resolve_form_page(self, info):
        form_page = None
        # TODO: don't catch everything
        try:
            form_page = FormPage.objects.get(id=self.page_id)
        except Exception as e:
            pass

        return form_page

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
    all_311 = DjangoFilterConnectionField(ThreeOneOneNode)
    all_official_document_pages = DjangoFilterConnectionField(
        OfficialDocumentPageNode)
    all_guide_pages = DjangoFilterConnectionField(GuidePageNode)
    all_form_pages = DjangoFilterConnectionField(FormPageNode)
    all_topic_page_topic_collections = DjangoFilterConnectionField(TopicPageTopicCollectionNode)
    all_service_page_topics = DjangoFilterConnectionField(ServicePageTopicNode)
    all_information_page_topics = DjangoFilterConnectionField(InformationPageTopicNode)
    all_official_document_page_topics = DjangoFilterConnectionField(OfficialDocumentPageTopicNode)
    all_guide_page_topics = DjangoFilterConnectionField(GuidePageTopicNode)

    def resolve_site_structure(self, resolve_info):
        site_structure = SiteStructure()
        return site_structure

    def resolve_page_revision(self, resolve_info, id=None):
        revision = graphene.Node.get_node_from_global_id(resolve_info, id)

        return revision


schema = graphene.Schema(query=Query)

import django.utils.translation
import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField
from graphene.types import Scalar
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, PageRevision
from django_filters import FilterSet, OrderingFilter

from base.models import TranslatedImage, ThreeOneOne, ServicePage, ServicePageContact, ServicePageTopic, ServicePageRelatedDepartments, InformationPageRelatedDepartments, ProcessPage, ProcessPageStep, ProcessPageContact, ProcessPageTopic, InformationPage, InformationPageContact, InformationPageTopic, DepartmentPage, DepartmentPageContact, DepartmentPageDirector, Theme, TopicCollectionPage, TopicPage, Contact, Location, ContactDayAndDuration, Department, DepartmentContact, TopicPageTopicCollection, OfficialDocumentPage, OfficialDocumentPageRelatedDepartments, OfficialDocumentPageTopic, OfficialDocumentPageOfficialDocument, GuidePage, GuidePageTopic, GuidePageRelatedDepartments, GuidePageContact

class StreamFieldType(Scalar):
    @staticmethod
    def serialize(dt):
        return [{'type': item.block_type, 'value': item.block.get_api_representation(item.value), 'id': item.id} for item in dt]


@convert_django_field.register(StreamField)
def convert_stream_field(field, registry=None):
    return StreamFieldType(description=field.help_text, required=not field.null)


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


class ContactDayAndDurationNode(DjangoObjectType):
    class Meta:
        model = ContactDayAndDuration
        interfaces = [graphene.Node]


class ContactNode(DjangoObjectType):
    class Meta:
        model = Contact
        interfaces = [graphene.Node]


class ServicePageContactNode(DjangoObjectType):
    class Meta:
        model = ServicePageContact
        interfaces = [graphene.Node]

class ServicePageTopicNode(DjangoObjectType):
    class Meta:
        model = ServicePageTopic
        interfaces = [graphene.Node]

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
    # related = graphene.List('api.schema.ServicePageNode')

    # def resolve_related(self, resolve_info, *args, **kwargs):
    #     return self.topic.servicepage_set.exclude(id=self.id)

    class Meta:
        model = ServicePage
        filter_fields = ['id', 'slug', 'live']
        interfaces = [graphene.Node]

class ProcessPageNode(DjangoObjectType):
    class Meta:
        model = ProcessPage
        filter_fields = ['id', 'slug', 'department', 'live']
        interfaces = [graphene.Node]

class InformationPageNode(DjangoObjectType):
    class Meta:
        model = InformationPage
        filter_fields = ['id', 'slug', 'live']
        interfaces = [graphene.Node]

class DepartmentPageNode(DjangoObjectType):
    class Meta:
        model = DepartmentPage
        filter_fields = ['id', 'slug', 'live']
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
    official_documents = DjangoFilterConnectionField(OfficialDocumentPageOfficialDocumentNode, filterset_class=OfficialDocumentFilter)

    class Meta:
        model = OfficialDocumentPage
        filter_fields = ['id', 'slug', 'live']
        interfaces = [graphene.Node]

class GuidePageNode(DjangoObjectType):
    class Meta:
        model = GuidePage
        filter_fields = ['id', 'slug', 'live']
        interfaces = [graphene.Node]

class PageRevisionNode(DjangoObjectType):
    as_service_page = graphene.NonNull(ServicePageNode)
    as_process_page = graphene.NonNull(ProcessPageNode)
    as_information_page = graphene.NonNull(InformationPageNode)
    as_department_page = graphene.NonNull(DepartmentPageNode)
    as_topic_page = graphene.NonNull(TopicNode)
    as_topic_collection_page = graphene.NonNull(TopicCollectionNode)
    as_official_document_page = graphene.NonNull(OfficialDocumentPageNode)

    def resolve_as_service_page(self, resolve_info, *args, **kwargs):
        return self.as_page_object();

    def resolve_as_process_page(self, resolve_info, *args, **kwargs):
        return self.as_page_object();

    def resolve_as_information_page(self, resolve_info, *args, **kwargs):
        return self.as_page_object();

    def resolve_as_department_page(self, resolve_info, *args, **kwargs):
        return self.as_page_object();

    def resolve_as_topic_page(self, resolve_info, *args, **kwargs):
        return self.as_page_object();

    def resolve_as_topic_collection_page(self, resolve_info, *args, **kwargs):
        return self.as_page_object();

    def resolve_as_official_document_page(self, resolve_info, *args, **kwargs):
        return self.as_page_object();

    class Meta:
        model = PageRevision
        filter_fields = ['id']
        interfaces = [graphene.Node]

class ProcessPageStepNode(DjangoObjectType):
    class Meta:
        model = ProcessPageStep
        interfaces = [graphene.Node]

class ProcessPageContactNode(DjangoObjectType):
    class Meta:
        model = ProcessPageContact
        interfaces = [graphene.Node]

class ProcessPageTopicNode(DjangoObjectType):
    class Meta:
        model = ProcessPageTopic
        interfaces = [graphene.Node]

class InformationPageContactNode(DjangoObjectType):
    class Meta:
        model = InformationPageContact
        interfaces = [graphene.Node]

class InformationPageTopicNode(DjangoObjectType):
    class Meta:
        model = InformationPageTopic
        interfaces = [graphene.Node]

class DepartmentPageContactNode(DjangoObjectType):
    class Meta:
        model = DepartmentPageContact
        interfaces = [graphene.Node]

class DepartmentPageDirectorNode(DjangoObjectType):
    class Meta:
        model = DepartmentPageDirector
        interfaces = [graphene.Node]

class OfficialDocumentPageTopicNode(DjangoObjectType):
    class Meta:
        model = OfficialDocumentPageTopic
        interfaces = [graphene.Node]



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

    service_page = graphene.Field(ServicePageNode, id=graphene.ID(), pk=graphene.Int(), slug=graphene.String(), show_preview=graphene.Boolean(default_value=False), language=Language())
    department_page = graphene.Node.Field(DepartmentPageNode)
    all_service_pages = DjangoFilterConnectionField(ServicePageNode)
    page_revision = graphene.Field(PageRevisionNode, id=graphene.ID())
    all_page_revisions = DjangoFilterConnectionField(PageRevisionNode)
    all_processes = DjangoFilterConnectionField(ProcessPageNode)
    all_information_pages = DjangoFilterConnectionField(InformationPageNode)
    all_department_pages = DjangoFilterConnectionField(DepartmentPageNode)
    all_themes = DjangoFilterConnectionField(ThemeNode)
    all_topics = DjangoFilterConnectionField(TopicNode)
    all_topic_collections = DjangoFilterConnectionField(TopicCollectionNode)
    all_departments = DjangoFilterConnectionField(DepartmentNode)
    all_311 = DjangoFilterConnectionField(ThreeOneOneNode)
    all_official_document_pages = DjangoFilterConnectionField(OfficialDocumentPageNode)
    all_guide_pages = DjangoFilterConnectionField(GuidePageNode)

    def resolve_page_revision(self, resolve_info, id=None):
        revision = graphene.Node.get_node_from_global_id(resolve_info, id)

        return revision

    def resolve_service_page(self, resolve_info, id=None, pk=None, slug=None, show_preview=None, language=None):
        if not language:
            request_lang = django.utils.translation.get_language_from_request(resolve_info.context)
            language = request_lang or Language.ENGLISH

        django.utils.translation.activate(language)
        resolve_info.context.LANGUAGE_CODE = django.utils.translation.get_language()

        if id:
            page = graphene.Node.get_node_from_global_id(resolve_info, id)
        elif pk:
            page = Page.objects.get(pk=pk).specific
        elif slug:
            page = Page.objects.get(slug=slug).specific
        else:
            raise Exception('Please provide id or pk')

        if show_preview:
            page = get_page_with_preview_data(page, resolve_info.context.session) or page

        return page


schema = graphene.Schema(query=Query)

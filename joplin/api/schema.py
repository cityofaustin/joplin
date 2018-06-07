import django.utils.translation
import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField
from graphene.types import Scalar
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from base.models import TranslatedImage, ThreeOneOne, ServicePage, ProcessPage, Theme, Topic, Contact, ServicePageContact, Location, ContactDayAndDuration, Department, DepartmentContact


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


class TopicNode(DjangoObjectType):
    class Meta:
        model = Topic
        filter_fields = ['id', 'slug', 'text']
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
    related = graphene.List('api.schema.ServicePageNode')

    def resolve_related(self, resolve_info, *args, **kwargs):
        return self.topic.services.exclude(id=self.id)

    class Meta:
        model = ServicePage
        filter_fields = ['id', 'slug', 'topic', 'topic__slug']
        interfaces = [graphene.Node]

class ProcessPageNode(DjangoObjectType):
    related = graphene.List('api.schema.ProcessPageNode')

    def resolve_related(self, resolve_info, *args, **kwargs):
        return self.topic.services.exclude(id=self.id)

    class Meta:
        model = ProcessPage
        filter_fields = ['id', 'slug', 'topic', 'topic__slug']
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
    all_service_pages = DjangoFilterConnectionField(ServicePageNode)

    process_page = graphene.Field(ProcessPageNode, id=graphene.ID(), pk=graphene.Int(), slug=graphene.String(), show_preview=graphene.Boolean(default_value=False), language=Language())
    all_process_pages = DjangoFilterConnectionField(ProcessPageNode)

    all_themes = DjangoFilterConnectionField(ThemeNode)
    all_topics = DjangoFilterConnectionField(TopicNode)
    all_departments = DjangoFilterConnectionField(DepartmentNode)
    all_311 = DjangoFilterConnectionField(ThreeOneOneNode)

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

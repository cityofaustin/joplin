import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField
from graphene.types import Scalar
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page

from base.models import ServicePage, Topic, Contact, ServicePageContact, Location, ContactDayAndDuration


class StreamFieldType(Scalar):
    @staticmethod
    def serialize(dt):
        return [{'type': item.block_type, 'value': item.block.get_api_representation(item.value), 'id': item.id} for item in dt]


@convert_django_field.register(StreamField)
def convert_stream_field(field, registry=None):
    return StreamFieldType(description=field.help_text, required=not field.null)


class TopicNode(DjangoObjectType):
    class Meta:
        model = Topic
        filter_fields = ['text']
        interfaces = [graphene.Node]


class LocationNode(DjangoObjectType):
    class Meta:
        model = Location
        interfaces = [graphene.Node]


class ContacDayAndDurationNode(DjangoObjectType):
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


class ServicePageNode(DjangoObjectType):
    class Meta:
        model = ServicePage
        filter_fields = ['id', 'slug', 'topic', 'topic__text']
        interfaces = [graphene.Node]


def get_page_with_preview_data(page, session):
    # Wagtail saves preview data in the session. We want to mimick what they're doing to generate the built-in preview.
    # https://github.com/wagtail/wagtail/blob/db6d36845f3f2c5d7009a22421c2efab9968aa24/wagtail/admin/views/pages.py#L544
    # TODO: This should be simpler. Instead of hijacking the wagtail admin, it'd probably be easier to create a new endpoint
    #       or have a graphql mutation do the work
    session_key = f'wagtail-preview-{page.pk}'
    preview_data, timestamp = session.get(session_key, [None, None])

    if preview_data:
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

    preview = graphene.Field(ServicePageNode, id=graphene.ID(), pk=graphene.Int(), show_preview=graphene.Boolean(default_value=True))
    page = graphene.Node.Field(ServicePageNode)
    pages = DjangoFilterConnectionField(ServicePageNode)

    def resolve_preview(self, resolve_info, id=None, pk=None, show_preview=None):
        if id:
            page = graphene.Node.get_node_from_global_id(resolve_info, id)
        elif pk:
            page = Page.objects.get(pk=pk).specific
        else:
            raise Exception('Please provide id or pk')

        return get_page_with_preview_data(page, resolve_info.context.session) if show_preview else page


schema = graphene.Schema(query=Query)

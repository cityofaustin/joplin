import graphene
from graphene_django import DjangoObjectType
from graphene_django.debug import DjangoDebug
from wagtail.core.models import PageRevision
import graphql_jwt
from api.schema import ServicePageNode, InformationPageNode, DepartmentPageNode, TopicNode, TopicCollectionNode, \
    OfficialDocumentPageNode, OfficialDocumentCollectionNode, NewsPageNode, EventPageNode, ContextualNavData, \
    GuidePageNode, FormContainerNode, LocationPageNode


class PageRevisionNode(DjangoObjectType):
    as_service_page = graphene.NonNull(ServicePageNode)
    as_information_page = graphene.NonNull(InformationPageNode)
    as_department_page = graphene.NonNull(DepartmentPageNode)
    as_topic_page = graphene.NonNull(TopicNode)
    as_topic_collection_page = graphene.NonNull(TopicCollectionNode)
    as_official_document_page = graphene.NonNull(OfficialDocumentPageNode)
    as_official_document_collection = graphene.NonNull(OfficialDocumentCollectionNode)
    as_guide_page = graphene.NonNull(GuidePageNode)
    as_form_container = graphene.NonNull(FormContainerNode)
    as_location_page = graphene.NonNull(LocationPageNode)
    as_event_page = graphene.NonNull(EventPageNode)
    as_news_page = graphene.NonNull(NewsPageNode)
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

    def resolve_as_news_page(self, resolve_info, *args, **kwargs):
        return self.as_page_object()

    def resolve_as_official_document_collection(self, resolve_info, *args, **kwargs):
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


# Allow users to request JWT token for authorization-protected resolvers
# https://django-graphql-jwt.domake.io/en/latest/quickstart.html
class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')
    page_revision = graphene.Field(PageRevisionNode, id=graphene.ID())

    def resolve_page_revision(self, resolve_info, id=None):
        revision = graphene.Node.get_node_from_global_id(resolve_info, id)
        return revision


preview_schema = graphene.Schema(query=Query, mutation=Mutation)

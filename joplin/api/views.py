from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from graphene_django.views import GraphQLView


class GetLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated only for GET requests"""
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET' and not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class PrivateGraphQLView(GetLoginRequiredMixin, GraphQLView):
    raise_exception = True
    pass

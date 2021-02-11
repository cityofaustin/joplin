from functools import wraps
from graphql_jwt.utils import get_credentials
from graphql_jwt.shortcuts import get_user_by_token


def jwt_token_decorator(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        token = get_credentials(request, **kwargs)
        if token is not None:
            request.user = get_user_by_token(token, request)
        return view_func(request, *args, **kwargs)
    return wrapped_view

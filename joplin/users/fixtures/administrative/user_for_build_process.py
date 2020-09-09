import os
from users.fixtures.helpers.create_fixture import create_fixture


def user_for_build_process():
    """
    A user for graphql api authentication.
    Should be loaded on all branches.
    """
    user_data = {
        "email": "api_user@austintexas.io",
        "is_superuser": True,
        "password": os.getenv("API_PASSWORD"),
        "first_name": "Build",
        "last_name": "Robot",
        "is_active": True,
        "is_staff": True,
    }

    return create_fixture(user_data, os.path.basename(__file__))

import os
from django.conf import settings
from django.core.exceptions import ValidationError
from users.fixtures.helpers.create_fixture import create_fixture
from groups.fixtures.test_cases.kitchen_sink import kitchen_sink
from django.contrib.auth.models import Group


# An user for API Testing.
# Should be loaded on "test" Joplin branch only.
def editor_for_test_env():
    user_data = {
        "email": "editor@austintexas.io",
        "is_superuser": False,
        "password": os.getenv("API_TEST_USER_PASSWORD"),
        "first_name": "Editor",
        "last_name": "Robot",
        "is_active": True,
        "is_staff": True,
    }

    editor_group = Group.objects.get(name="Editors")
    # Extra safety check
    if settings.IS_STAGING or settings.IS_PRODUCTION:
        raise ValidationError("Do not load test user onto staging or production")
    else:
        return create_fixture(user_data, os.path.basename(__file__), [kitchen_sink(), editor_group])

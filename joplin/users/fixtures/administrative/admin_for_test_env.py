import os
from django.conf import settings
from django.core.exceptions import ValidationError
from users.fixtures.helpers.create_fixture import create_fixture


# An user for API Testing.
# Should be loaded on "test" Joplin branch only.
def admin_for_test_env():
    user_data = {
        "email": "apitest@austintexas.io",
        "is_superuser": True,
        "password": os.getenv("API_TEST_USER_PASSWORD"),
        "first_name": "API Test",
        "last_name": "Robot",
        "is_active": True,
        "is_staff": True,
    }

    # Extra safety check
    if settings.IS_STAGING or settings.IS_PRODUCTION:
        raise ValidationError("Do not load test user onto staging or production")
    else:
        return create_fixture(user_data, os.path.basename(__file__))

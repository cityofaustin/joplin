import os
from django.conf import settings
from django.core.exceptions import ValidationError
from users.fixtures.helpers.create_fixture import create_fixture


# An user for API Testing.
# Should be loaded on "test" Joplin branch only.
def superadmin():
    topic_collection = kitchen_sink_topic_collection.kitchen_sink()

    user_data = {
        "email": "admin@austintexas.io",
        "is_superuser": True,
        "password": os.get_env("SUPERADMIN_USER_PASSWORD"),
        "first_name": "City of",
        "last_name": "Austin",
    }

    # Extra safety check
    if settings.IS_STAGING or settings.IS_PRODUCTION:
        raise ValidationError("Do not load superadmin onto staging or production")
    else:
        return create_fixture(user_data, os.path.basename(__file__))

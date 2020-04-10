import os
from snippets.theme.fixtures.helpers.create_fixture import create_fixture


def kitchen_sink():
    theme_data = {
        "text": "Kitchen sink theme [en]",
        "text_es": "Kitchen sink theme [es]"
    }

    return create_fixture(theme_data, os.path.basename(__file__))

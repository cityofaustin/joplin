import os
from pages.service_page.fixtures.helpers.create_fixture import create_fixture
import pages.service_page.fixtures.helpers.components as components
from pages.topic_page.fixtures.test_cases import kitchen_sink as kitchen_sink_topic


# A "kitchen sink" service page
def kitchen_sink():
    topic = kitchen_sink_topic.kitchen_sink()
    steps = components.steps_with_appblocks.extend(components.steps_2).extend(components.step_with_options)

    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": components.home(),
        "coa_global": False,
        "title": "Kitchen sink service page [en]",
        "title_es": "Kitchen sink service page [es]",
        "slug": "kitchen-sink-service-page",
        "add_topics": {
            "topics": [topic]
        },
        "short_description": "Kitchen sink service page short description [en]",
        "dynamic_content": components.dynamic_content,
        "steps": steps,
    }

    return create_fixture(page_data, os.path.basename(__file__))

import os
from pages.service_page.fixtures.helpers.create_fixture import create_fixture
import pages.service_page.fixtures.helpers.components as components
from pages.topic_page.fixtures.test_cases import kitchen_sink as kitchen_sink_topic
from groups.fixtures.test_cases import kitchen_sink as kitchen_sink_department

# A "kitchen sink" service page
def kitchen_sink():
    topic = kitchen_sink_topic.kitchen_sink()
    steps = components.steps_with_appblocks
    steps.extend(components.steps_2)
    steps.extend(components.step_with_options)
    steps.extend(components.step_with_1_location())
    department = kitchen_sink_department.kitchen_sink()

    page_data = {
        "imported_revision_id": None,
        "live": True,
        "published": True,
        "parent": components.home(),
        "coa_global": False,
        "title": "Kitchen sink service page [en]",
        "title_es": "Kitchen sink service page [es]",
        "slug": "kitchen-sink-service-page",
        "add_topics": {
            "topics": [topic]
        },
        "add_departments": {
            "departments": [department]
        },
        "short_description": "Kitchen sink service page short description [en]",
        "additional_content": components.additional_content,
        'dynamic_content': components.dynamic_content_list,
        "steps": steps,
    }

    return create_fixture(page_data, os.path.basename(__file__))

import os
from groups.fixtures.helpers.create_fixture import create_fixture
from pages.department_page.fixtures.test_cases import kitchen_sink as kitchen_sink_department


# A "kitchen sink" department group
def kitchen_sink():
    department_page = kitchen_sink_department.kitchen_sink()

    group_data = {
        "name": "Kitchen sink department",
        "department_page": department_page
    }

    return create_fixture(group_data, os.path.basename(__file__))

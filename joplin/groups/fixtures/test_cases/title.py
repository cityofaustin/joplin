import os
from groups.fixtures.helpers.create_fixture import create_fixture


# A Department group with only a title
def title():
    group_data = {
        "name": "Municipal Court"
    }

    return create_fixture(group_data, os.path.basename(__file__))

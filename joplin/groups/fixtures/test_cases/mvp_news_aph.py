import os
from groups.fixtures.helpers.create_fixture import create_fixture


# A department group for APH as an example for mvp news
# https://share.goabstract.com/ac28fbf0-0ef7-448c-98d7-b652d936a2f8
def mvp_news_aph():
    group_data = {
        "name": "Austin Public Health"
    }

    return create_fixture(group_data, os.path.basename(__file__))

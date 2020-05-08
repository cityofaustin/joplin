import os
from groups.fixtures.helpers.create_fixture import create_fixture
from pages.department_page.fixtures.helpers.components import mvp_news_cpio as department_page_cpio


# A department group for CPIO as an example for mvp news
# https://share.goabstract.com/ac28fbf0-0ef7-448c-98d7-b652d936a2f8
def mvp_news_cpio():
    department_page = department_page_cpio()

    group_data = {
        "name": "Communications and Public Information Office",
        "department_page": department_page
    }

    return create_fixture(group_data, os.path.basename(__file__))

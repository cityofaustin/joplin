import os
from pages.news_page.fixtures.helpers.create_fixture import create_fixture
import pages.news_page.fixtures.helpers.components as components
import snippets.contact.fixtures.helpers.components as contact_components
import pages.department_page.fixtures.helpers.components as department_page_components
from groups.fixtures.test_cases.mvp_news_cpio import mvp_news_cpio


# A news page with data that matches MVP dev handoff test data
# Janis:
# https://app.abstract.com/projects/065fcabf-a46a-4688-a858-83ce2117b16c/branches/6b5fab74-d723-4f52-a22d-4d4260faf803/collections/e5d5024b-7a3e-4f30-8179-aa88db70d29f
# Joplin:
# https://share.goabstract.com/501e9b40-3cb4-48ce-8532-dbd25cbcac6e?collectionLayerId=4e370572-0864-4ec8-892e-4362558f4267&mode=design
def written_by_CPIO_written_for_APH():
    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": components.home(),
        "coa_global": False,
        "title": components.mvp_news_title,
        "slug": "mvp-news",
        "body": components.mvp_news_body,
        "written_for_department": department_page_components.mvp_news_aph(),
        "contact": contact_components.mvp_news_contact(),
        "add_departments": {
            "departments": [mvp_news_cpio()]
        },
    }

    return create_fixture(page_data, os.path.basename(__file__))

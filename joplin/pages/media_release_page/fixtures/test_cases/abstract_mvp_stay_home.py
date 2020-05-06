import os
from pages.media_release_page.fixtures.helpers.create_fixture import create_fixture
import pages.media_release_page.fixtures.helpers.components as components


# A media release page with data that matches MVP dev handoff test data
# Janis:
# https://app.abstract.com/projects/065fcabf-a46a-4688-a858-83ce2117b16c/branches/6b5fab74-d723-4f52-a22d-4d4260faf803/collections/e5d5024b-7a3e-4f30-8179-aa88db70d29f
# Joplin:
# https://share.goabstract.com/501e9b40-3cb4-48ce-8532-dbd25cbcac6e?collectionLayerId=4e370572-0864-4ec8-892e-4362558f4267&mode=design
def abstract_mvp_stay_home():
    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": components.home(),
        "coa_global": False,
        "title": "Health Authorities Continue to Stress the Importance of Stay at Home & Social Distancing",
        "slug": "abstract-mvp-stay-home",
        "body": components.abstract_mvp_stay_home_body,
        # todo: another department
        # todo: contact
    }

    return create_fixture(page_data, os.path.basename(__file__))

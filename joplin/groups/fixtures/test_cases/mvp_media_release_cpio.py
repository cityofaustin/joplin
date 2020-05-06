import os
from groups.fixtures.helpers.create_fixture import create_fixture


# A department group for CPIO as an example for mvp media releases
# https://share.goabstract.com/ac28fbf0-0ef7-448c-98d7-b652d936a2f8

def mvp_media_release_cpio():
    group_data = {
        "name": "Communications and Public Information Office"
    }

    return create_fixture(group_data, os.path.basename(__file__))

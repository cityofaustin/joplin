import os, json, requests, logging
from django.conf import settings
from pages.home_page.models import HomePage

logger = logging.getLogger('joplin')


def publish_v3(page_ids=[]):
    # TODO: we want to extract the publish_janis_branch() for each page_id that we're publishing.
    # That logic must happen earlier in the collect_pages logic.
    # Even though this will work for now, it should not be hardcoded to be the first HomePage object.
    publish_janis_branch = HomePage.objects.first().publish_janis_branch()

    if not publish_janis_branch:
        logger.info("publish_janis_branch must be set in order to publish.")
        return None

    headers = {
        "x-api-key": settings.PUBLISHER_V2_API_KEY,
        "content-type": "application/json",
    }
    url = settings.PUBLISHER_V2_URL
    data = {
        "janis_branch": publish_janis_branch,
        "page_ids": page_ids,
        "joplin_appname": settings.APPNAME,
        "env_vars": {
            "REACT_STATIC_PREFETCH_RATE": "5",
        },
        "build_type": "rebuild",
    }
    publisher_res = requests.post(url, data=json.dumps(data), headers=headers)
    logger.info("publish_v3() Starting task")
    logger.info(publisher_res.json())

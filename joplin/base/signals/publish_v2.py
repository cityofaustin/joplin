import os, json, requests, logging
from django.conf import settings
from base.models.site_settings import JanisBranchSettings

logger = logging.getLogger('joplin')


def publish_v2(page_ids=[]):
    publish_janis_branch = getattr(JanisBranchSettings.objects.first(), 'publish_janis_branch')
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
        "build_type": "all_pages",
    }
    publisher_res = requests.post(url, data=json.dumps(data), headers=headers)
    logger.info("publish_v2() Starting task")
    logger.info(publisher_res.json())

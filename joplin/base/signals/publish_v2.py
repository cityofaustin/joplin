import os, json, requests, logging
from django.conf import settings
from base.models.site_settings import JanisBranchSettings

logger = logging.getLogger(__name__)


def publish_v2(page_ids=[]):
    if settings.ISLOCAL:
        logger.debug("Running locally, skipping publisher_v2 invocation")
        return None

    publish_janis_branch = getattr(JanisBranchSettings.objects.first(), 'publish_janis_branch')
    if not publish_janis_branch:
        logger.debug("publish_janis_branch must be set in order to publish.")
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
    logger.debug("publish_v2() Starting task")
    logger.debug(publisher_res.json())

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from wagtail.core.signals import page_published, page_unpublished
from base.models.site_settings import JanisBranchSettings

import os
import logging
import requests
import json
logger = logging.getLogger(__name__)


def netlify_publish():
    logger.debug("netlify_publish() Starting task")
    try:
        publish_janis_branch = getattr(JanisBranchSettings.objects.first(), 'publish_janis_branch')
    except:
        publish_janis_branch = None

    if publish_janis_branch:
        requests.post(
            url=f"{os.getenv('COA_PUBLISHER_URL')}/publish",
            data=json.dumps({
                "janis_branch": publish_janis_branch,
                "CMS_API": settings.CMS_API,
            }),
        )
        logger.debug("Sent publish request to coa-publisher.")
    else:
        logger.debug("Missing vars. Not publishing")

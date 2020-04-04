from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from wagtail.core.signals import page_published, page_unpublished
from pages.home_page.models import HomePage

import os
import logging
import requests
import json
logger = logging.getLogger(__name__)


def netlify_publish():
    logger.debug("netlify_publish() Starting task")
    try:
        # TODO: we want to extract the publish_janis_branch() for each page_id that we're publishing.
        # That logic must happen earlier in the collect_pages logic.
        # Even though this will work for now, it should not be hardcoded to be the first HomePage object.
        publish_janis_branch = HomePage.objects.first().publish_janis_branch()
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

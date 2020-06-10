import os, json, requests, logging
from datetime import datetime
from pytz import timezone
from django.conf import settings
from pages.home_page.models import HomePage
from django.shortcuts import get_object_or_404
from rest_framework_api_key.models import APIKey

logger = logging.getLogger('joplin')


def publish(pages, primary_page=None):
    if not settings.PUBLISH_ENABLED:
        return

    # TODO: we want to extract the publish_janis_branch() for each page_id that we're publishing (for example, if we start publishing to different sites).
    # That logic must happen earlier in the collect_pages logic.
    # Even though this will work for now, it should not be hardcoded to be the first HomePage object.
    publish_janis_branch = HomePage.objects.first().publish_janis_branch()

    if not publish_janis_branch:
        logger.info("publish_janis_branch must be set in order to publish.")
        return None

    api_key = APIKey.objects.create_key(
        name=f"publisher-{datetime.now(timezone('US/Central')).isoformat()}"
    )[1]

    headers = {
        "x-api-key": settings.PUBLISHER_V2_API_KEY,
        "content-type": "application/json",
    }
    url = settings.PUBLISHER_V2_URL
    data = {
        "janis_branch": publish_janis_branch,
        "pages": pages,
        "joplin_appname": settings.APPNAME,
        "api_key": api_key,
        "env_vars": {
            "REACT_STATIC_PREFETCH_RATE": "0",
        },
        "build_type": "rebuild",
    }
    res = requests.post(url, data=json.dumps(data), headers=headers)
    if res.status_code != 200:
        logger.error(f"publish_request failed with status {res.status_code}")
        logger.error(f"message: {res.json()['message']}")
    elif primary_page:
        res_data = res.json()
        publish_request_pk = res_data['pk']
        publish_request_sk = res_data['sk']
        primary_page.publish_request_pk = publish_request_pk
        primary_page.publish_request_sk = publish_request_sk
        primary_page.publish_request_enqueued = True
        logger.info(f"published() pk={publish_request_pk}, sk={publish_request_sk}")
        primary_page.save()

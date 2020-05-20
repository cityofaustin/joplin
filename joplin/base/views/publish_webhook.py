import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from wagtail.core.models import Page

import logging
logger = logging.getLogger('joplin')


'''
    Update "publish*" fields for pages that triggered publish requests.
'''
@require_POST
@csrf_exempt
def publish_webhook(request):
    body = json.loads(request.body)
    pages = body["pages"]

    # Update pages in order, in case subsequent publish/unpublish requests overwrote each other.
    sort(pages, key=lambda page: page["timestamp"])
    for page_data in pages:
        if page_data["triggered_build"] and page_data["is_page"]:
            id = page_data["id"]
            try:
                page = get_object_or_404(Page, id=id)
                if page_data["action"] == "published":
                    page.published = True
                elif page_data["action"] == "unpublished":
                    page.published = False
                page.publish_request_pk = None
                page.publish_request_sk = None
                page.publish_request_enqueued = False
                page.save()
            except Http404:
                logger.error(f"Couldn't find a page with id={id}")
    return 200

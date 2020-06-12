from rest_framework.decorators import api_view, permission_classes
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_api_key.models import APIKey
from rest_framework.response import Response
import json
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from wagtail.core.models import Page


import logging
logger = logging.getLogger('joplin')


'''
    Updates "publish_*" fields in base_model for pages that triggered publish requests.
'''
@api_view(['POST'])
@permission_classes([HasAPIKey])
def publish_succeeded(request):
    body = json.loads(request.body)
    pages = body["pages"]

    # Clean up publish_request api_keys when we're done using them
    try:
        for api_key in body["api_keys"]:
            APIKey.objects.get_from_key(api_key).delete()
    except APIKey.DoesNotExist:
        logger.error(f"Couldn't find jwtToken with prefix {api_key[:8]}")

    # Update pages in order, in case subsequent publish/unpublish requests overwrote each other.
    pages.sort(key=lambda page: page["timestamp"])
    for page_data in pages:
        if page_data["triggered_build"] and page_data["is_page"]:
            id = page_data["id"]
            try:
                page = get_object_or_404(Page, id=id).specific
                # "published" and "unpublished" are the only possible actions for a page that triggered_build
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
    return Response(200)

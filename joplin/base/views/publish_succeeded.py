from rest_framework.decorators import api_view, permission_classes
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_api_key.models import APIKey
from rest_framework.response import Response
import json
import threading
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from wagtail.core.models import Page


import logging
logger = logging.getLogger('joplin')


@api_view(['POST'])
@permission_classes([HasAPIKey])
def publish_succeeded(request):
    '''
        Updates "publish_*" fields in base_model for pages that triggered publish requests.
        This is a "fire and forget" endpoint. Publisher doesn't care what happens to the page data once it reaches Joplin.
        Page data is processed in a separate thread. The code finishes executing after Publisher gets its response.
        Otherwise if we update more than 200 documents, this endpoint would time out.
            Parameters:
                request.body.pages (list of page_data)
                request.body.api_keys (list of str)
            Returns:
                Response (int): always return 200 success code.
    '''
    body = json.loads(request.body)
    pages = body["pages"]
    api_keys = body["api_keys"]
    threading.Thread(target=handle_publish_success, args=(pages,api_keys)).start()

    return Response(200)


def handle_publish_success(pages, api_keys):
    '''
        Updates "publish_*" fields in base_model for pages that triggered publish requests.
        Deletes the APIKeys that were used by Publisher to access this endpoint.
        (Publisher only used 1 APIKey to access this endpoint. But a BLD could have multiple APIKeys if there are multiple REQs (each with their own APIKey) in a single BLD.)

            Parameters:
                pages (list of page_data): metadata about pages that were published by Publisher.
                api_keys (list of str): api_keys used by Publisher to access this endpoint protected by @permission_classes([HasAPIKey])
            Returns:
                None
    '''
    # Update pages in order, in case subsequent publish/unpublish requests overwrote each other.
    pages.sort(key=lambda page: page["timestamp"])
    for page_data in pages:
        if page_data["triggered_build"] and page_data["is_page"]:
            id = page_data["id"]
            try:
                page = get_object_or_404(Page, id=id).specific
                update_page_after_publish_success(page, page_data["action"])
            except Http404:
                logger.error(f"Couldn't find a page with id={id}")

    # Clean up publish_request api_keys when we're done using them
    try:
        for api_key in api_keys:
            APIKey.objects.get_from_key(api_key).delete()
    except APIKey.DoesNotExist:
        logger.error(f"Couldn't find jwtToken with prefix {api_key[:8]}")


def update_page_after_publish_success(page, action):
    '''
        Updates "publish_*" fields in base_model for pages that triggered publish requests.

            Parameters:
                page (Page): a Page that triggered a build REQ to publisher
                action (str): "published" and "unpublished" are the only possible actions for a page that triggered_build
            Returns:
                None
    '''
    if action == "published":
        page.published = True
    elif action == "unpublished":
        page.published = False
    page.publish_request_pk = None
    page.publish_request_sk = None
    page.publish_request_enqueued = False
    page.save()

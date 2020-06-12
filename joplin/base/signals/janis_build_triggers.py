import requests, json
from datetime import datetime
from pytz import timezone
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from wagtail.core.signals import page_published, page_unpublished
from graphene import Node
from wagtail.core.models import Page
from wagtail.admin.models import get_object_usage
from rest_framework_api_key.models import APIKey

from snippets.contact.models import Contact
from pages.guide_page.models import GuidePage
from wagtail.documents.models import Document
from pages.home_page.models import HomePage


import logging
logger = logging.getLogger('joplin')


'''
Gets data from a page that is required to send to the Publisher.

returns {
    id: Int, the page_id used by wagtail.
    global_id: String, a hashed id used to query against graphql api
    triggered_build: Boolean, was this the page that triggered the publish request?
    action:
        "published" - publish action for itself and other pages
        "unpublished" - this page triggered the unpublish action for itself and other pages
        "updated_by_snippet" - this page was updated by a snippet being saved or deleted
        "saved" - a snippet is being saved, has no impact on Janis itself, but it could result in pages getting "secondary_publish_by_snippet"
        "deleted" - a snippet is being deleted, has no impact on Janis itself, but it could result in pages getting "secondary_publish_by_snippet"
    is_page: Boolean, is it a page as opposed to a snippet?
    content_type: String, which specific content_type (this is more for logging)
    author: Int, the id of the author of the latest revision
}
TODO: Figure out what format global_id should be in order to run queries with it.
The current global_id is basically a placeholder.
'''
def get_page_data(page, triggered_build, action):
    latest_revision = page.get_latest_revision()
    # imported pages may not have a latest_revision yet.
    if latest_revision:
        author = latest_revision.user.id
    else:
        author = None
    return {
        "id": page.id,
        "global_id": Node.to_global_id(page.content_type.name, page.id),
        "triggered_build": triggered_build,
        "action": action,
        "is_page": True,
        "content_type": page.specific_class.get_verbose_name(),
        "author": author,
    }


def collect_pages(primary_page, action):
    # does this work on page deletion? pages arent deleted right, just unpublished?
    """
    :param primary_page: the page that triggered the publish/unpublish
    :return: pages: an array of the data from all pages impacted by the publish/unpublish event
    """
    pages = [
        get_page_data(primary_page, True, action)
    ]
    primary_id = primary_page.id
    primary_content_type = primary_page.specific_class.get_verbose_name()
    page_set = get_object_usage(primary_page)
    # https://github.com/wagtail/wagtail/blob/master/wagtail/admin/models.py#L15
    # get_object_usage will also return the wagtail_page itself
    for page in page_set:
        # Primary page is also included in page_set. Don't re-add primary_page data.
        if not (page.id == primary_id):
            pages.append(get_page_data(page, False, action))

    if primary_content_type == 'Service Page' or primary_content_type == 'Information Page':
        guide_page_data = get_page_data_from_guides(primary_id, action)
        pages.extend(guide_page_data)
    return pages


def collect_pages_from_snippet(instance, action):
    """
    :param instance: the snippet that has been altered
    :return: an array of global page ids
    """
    snippet_data = {
        "id": instance.id,
        "global_id": None,
        "triggered_build": True,
        "action": action,
        "is_page": False,
        "content_type": instance.__class__.__name__,
        "author": None,  # TODO: is there a way to get the last editor of a snippet?
    }
    pages = [snippet_data]
    page_set = instance.get_usage()
    for page in page_set:
        pages.append(get_page_data(page, False, "updated_by_snippet"))
    return pages


def get_page_data_from_guides(changed_id, action):
    """
    Service Pages and information Pages don't know they are on Guides. So what happens if one is updated?
    Until we know better, this will go through all our guide pages and check if the page that is changed is in
    one of the guide's sections
    :param changed_id: id of the page that was published / unpublished
    :return: page_data for Guide Pages that include that page
    """
    pages = []
    all_guides = GuidePage.objects.all()
    for g in all_guides:
        for s in g.sections:
            # s.value.items() is an ordered dict
            list_of_values = list(s.value.items())
            # the pages are the 5th tuple
            section_pages = list_of_values[4][1]
            for page in section_pages:
                if changed_id == page.id:
                    pages.append(get_page_data(g, False, action))
    return pages


@receiver(page_published)
def page_published_signal(sender, **kwargs):
    # for the future, setting up a way to check if the title changed
    # https://stackoverflow.com/questions/1355150/when-saving-how-can-you-check-if-a-field-has-changed
    # because if the title didnt change, pages that contain links to the published page don't need to be updated
    action = "published"
    primary_page = Page.objects.get(id=kwargs['instance'].id)
    pages = collect_pages(primary_page, action)
    publish(pages, primary_page)


@receiver(page_unpublished)
def page_unpublished_signal(sender, **kwargs):
    action = "unpublished"
    primary_page = Page.objects.get(id=kwargs['instance'].id)
    pages = collect_pages(primary_page, action)
    publish(pages, primary_page)


# TODO: we can probably feed a list of models to attach the hook to
# more ideas here
# we might want to log but not trigger a build? need some sort of queue
@receiver(post_save, sender=Document)
@receiver(post_save, sender=Contact)
def handle_post_save_signal(sender, **kwargs):
    action = "saved"
    pages = collect_pages_from_snippet(kwargs['instance'], action)
    publish(pages)


@receiver(post_delete, sender=Document)
@receiver(post_delete, sender=Contact)
def handle_post_delete_signal(sender, **kwargs):
    action = "deleted"
    pages = collect_pages_from_snippet(kwargs['instance'], action)
    publish(pages)


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

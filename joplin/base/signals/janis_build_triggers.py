from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from wagtail.core.signals import page_published, page_unpublished
from graphene import Node
from wagtail.core.models import Page
from wagtail.admin.utils import get_object_usage

from base.models import Contact, Location, Map
from wagtail.documents.models import Document
from base.signals.aws_publish import get_http_request, create_build_aws
from base.signals.netlify_publish import netlify_publish

import logging
logger = logging.getLogger(__name__)

JANIS_SLUG_URL = settings.JANIS_SLUG_URL


def trigger_build(sender, pages_ids, action='saved', instance=None):
    print(pages_ids)
    """
    triggers different build process depending on environment
    source = name of snippet or object triggering build
    """
    trigger_object = instance
    logger.debug(f'{trigger_object} {action}, triggering build')
    if settings.ISSTAGING or settings.ISPRODUCTION:
        create_build_aws(sender, instance, request=get_http_request())
    elif settings.ISREVIEW:
        netlify_publish()


def collect_pages(instance):
    """
    :param instance: the page or snippet that has been altered
    :return: an array of global page ids -- note this may need to be a dictionary of page ids and type?
    """
    global_ids = []
    print(instance)
    wagtail_page = Page.objects.get(id=instance.id)
    page_set = get_object_usage(wagtail_page)
    for page in page_set:
        print(page, page.id, page.content_type)
        global_ids.append(Node.to_global_id(page.content_type.name, page.id))
    global_page_id = Node.to_global_id(instance.get_verbose_name(), instance.id)
    global_ids.append(global_page_id)

    return global_ids

# TODO: we can probably feed a list of models to attach the hook to
# more ideas here
# we might want to log but not trigger a build? need some sort of queue
@receiver(post_save, sender=Document)
@receiver(post_save, sender=Contact)
@receiver(post_save, sender=Location)
@receiver(post_save, sender=Map)
def handle_post_save_signal(sender, **kwargs):
    print(kwargs['instance'], type(kwargs['instance']))
    usage = kwargs['instance'].get_usage()
    print(usage)
    pages_ids = []
    for p in usage:
        page_id = Node.to_global_id(p.content_type.name, p.id)
        pages_ids.append(page_id) # do we need to then check what pages these are in?

    trigger_build(sender, pages_ids, instance=kwargs['instance'])


@receiver(page_published)
def page_published_signal(sender, **kwargs):
    pages_global_ids = collect_pages(kwargs['instance'])
    trigger_build(sender, pages_global_ids, action='published', instance=kwargs['instance'])


@receiver(page_unpublished)
def page_unpublished_signal(sender, **kwargs):
    pages_global_ids = collect_pages(kwargs['instance'])
    trigger_build(sender, pages_global_ids, action='unpublished', instance=kwargs['instance'])

@receiver(post_delete, sender=Document)
@receiver(post_delete, sender=Contact)
@receiver(post_delete, sender=Location)
@receiver(post_delete, sender=Map)
def handle_post_delete_signal(sender, **kwargs):
    print(kwargs['instance'], type(kwargs['instance']))
    usage = kwargs['instance'].get_usage()
    print(usage)
    pages_ids = []
    for p in usage:
        page_id = Node.to_global_id(p.content_type.name, p.id)
        pages_ids.append(page_id) # do we need to then check what pages these are in?
    trigger_build(sender, pages_ids, action='deleted', instance=kwargs['instance'])

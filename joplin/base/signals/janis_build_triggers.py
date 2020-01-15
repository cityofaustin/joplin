from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from wagtail.core.signals import page_published, page_unpublished
from graphene import Node

import heroku3
from heroku3.models.build import Build

import boto3

from base.models import Contact, Location, Map
from wagtail.documents.models import Document
from base.signals.aws_publish import get_http_request, create_build_aws
from base.signals.netlify_publish import netlify_publish

import logging
logger = logging.getLogger(__name__)

JANIS_SLUG_URL = settings.JANIS_SLUG_URL


def trigger_build(sender, pages_ids, action='saved', instance=None):
    print(pages_ids)
    # >> > graphene.Node.to_global_id('InformationPage', 28)
    # 'SW5mb3JtYXRpb25QYWdlOjI4'
    # >> > graphene.Node.to_global_id('Information page', 28)
    # 'SW5mb3JtYXRpb24gcGFnZToyOA=='
    # >> > graphene.Node.to_global_id('information', 28)
    # 'aW5mb3JtYXRpb246Mjg='
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


# TODO: we can probably feed a list of models to attach the hook to
# more ideas here
# we might want to log but not trigger a build? need some sort of queue
@receiver(post_save, sender=Document)
@receiver(post_save, sender=Contact)
@receiver(post_save, sender=Location)
@receiver(post_save, sender=Map)
def handle_post_save_signal(sender, **kwargs):
    usage = kwargs['instance'].get_usage()
    pages_ids = []
    for p in usage:
        page_id = Node.to_global_id(p.content_type.name, p.id)
        pages_ids.append(page_id)

    trigger_build(sender, pages_ids, instance=kwargs['instance'])


@receiver(page_published)
def page_published_signal(sender, **kwargs):
    # this does not take into account all the pages its connected to
    page_global_id = Node.to_global_id(kwargs['instance'].get_verbose_name(), kwargs['instance'].id)
    trigger_build(sender, page_global_id, action='published', instance=kwargs['instance'])


@receiver(page_unpublished)
def page_unpublished_signal(sender, **kwargs):
    page_global_id = Node.to_global_id(kwargs['instance'].get_verbose_name(), kwargs['instance'].id)
    trigger_build(sender, page_global_id, action='unpublished', instance=kwargs['instance'])

# TODO: should we add hooks for the above snippets/models on post delete as well? <--- ?
@receiver(post_delete, sender=Document)
def document_post_delete_signal(sender, **kwargs):
    page_global_id = Node.to_global_id(kwargs['instance'].get_verbose_name(), kwargs['instance'].id)
    trigger_build(sender, page_global_id, action='deleted', instance=kwargs['instance'])

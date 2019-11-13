from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from wagtail.core.signals import page_published, page_unpublished

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


def trigger_build(sender, action='saved', instance=None):
    """
    triggers different build process depending on environment
    source = name of snippet or object triggering build
    """
    trigger_object = instance
    logger.debug(f'{trigger_object} {action}, triggering build')
    if settings.ISSTAGING or settings.ISPRODUCTION:
        create_build_aws(sender, kwargs['instance'], request=get_http_request())
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
    trigger_build(sender, instance=kwargs['instance'])


@receiver(page_published)
def page_published_signal(sender, **kwargs):
    trigger_build(sender, action='published', instance=kwargs['instance'])


@receiver(page_unpublished)
def page_unpublished_signal(sender, **kwargs):
    trigger_build(sender, action='unpublished', instance=kwargs['instance'])

# TODO: should we add hooks for the above snippets/models on post delete as well?
@receiver(post_delete, sender=Document)
def document_post_delete_signal(sender, **kwargs):
    trigger_build(sender, action='deleted', instance=kwargs['instance'])

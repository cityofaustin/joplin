from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from wagtail.core.signals import page_published, page_unpublished

from base.models import Contact, Location, Map

import os, logging, requests, json
logger = logging.getLogger(__name__)

def netlify_publish():
    logger.debug("netlify_publish() Starting task")
    CI_COA_PUBLISHER_URL = os.getenv("CI_COA_PUBLISHER_URL")
    requests.post(
        url=f"CI_COA_PUBLISHER_URL/publish",
        data=json.dumps({

        }),
    )

# By creating a signal reciever for each snippet model we have, we can avoid
# needing to filter out large amounts of unwanted calls in our function logic
@receiver(post_save, sender=Contact)
def contact_post_save_signal(sender, **kwargs):
    logger.debug(f'contact_post_save {sender}')
    create_build_aws("Contact", kwargs['instance'], request=get_http_request())

@receiver(post_save, sender=Location)
def location_post_save_signal(sender, **kwargs):
    logger.debug(f'location_post_save {sender}')
    create_build_aws("Location", kwargs['instance'], request=get_http_request())

@receiver(post_save, sender=Map)
def map_post_save_signal(sender, **kwargs):
    logger.debug(f'map_post_save {sender}')
    create_build_aws("Map", kwargs['instance'], request=get_http_request())

@receiver(page_published)
def page_published_signal(sender, **kwargs):
    logger.debug(f'page_published {sender}')
    create_build_aws("Page", kwargs['instance'], publish_action='published', request=get_http_request())

@receiver(page_unpublished)
def page_unpublished_signal(sender, **kwargs):
    logger.debug(f'page_unpublished {sender}')
    create_build_aws("Page", kwargs['instance'], publish_action='unpublished', request=get_http_request())

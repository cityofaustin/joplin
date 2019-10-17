from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from wagtail.core.signals import page_published, page_unpublished
from base.models import Contact, Location, Map
from base.models.site_settings import JanisBranchSettings

import os, logging, requests, json
logger = logging.getLogger(__name__)

def netlify_publish():
    logger.debug("netlify_publish() Starting task")
    try:
        publish_janis_branch = getattr(JanisBranchSettings.objects.first(), 'publish_janis_branch')
    except:
        publish_janis_branch = None

    # Can't publish from LOCAL environment. A deployed Janis couldn't ping your localhost:8000
    if publish_janis_branch:
        requests.post(
            url=f"{os.getenv("CI_COA_PUBLISHER_URL")}/publish",
            data=json.dumps({
                "janis_branch": publish_janis_branch,
                "CMS_API": settings.CMS_API,
            }),
        )
        logger.debug("Sent publish request to coa-publisher.")
    else:
        logger.debug("Missing vars. Not publishing")


# By creating a signal reciever for each snippet model we have, we can avoid
# needing to filter out large amounts of unwanted calls in our function logic
@receiver(post_save, sender=Contact)
def contact_post_save_signal(sender, **kwargs):
    logger.debug(f'contact_post_save {sender}')
    netlify_publish()

@receiver(post_save, sender=Location)
def location_post_save_signal(sender, **kwargs):
    logger.debug(f'location_post_save {sender}')
    netlify_publish()

@receiver(post_save, sender=Map)
def map_post_save_signal(sender, **kwargs):
    logger.debug(f'map_post_save {sender}')
    netlify_publish()

@receiver(page_published)
def page_published_signal(sender, **kwargs):
    logger.debug(f'page_published {sender}')
    netlify_publish()

@receiver(page_unpublished)
def page_unpublished_signal(sender, **kwargs):
    logger.debug(f'page_unpublished {sender}')
    netlify_publish()

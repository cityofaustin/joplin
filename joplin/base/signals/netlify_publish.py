from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from wagtail.core.signals import page_published, page_unpublished
from base.models import Contact, Location, Map
from base.models.site_settings import JanisBranchSettings

import os, logging, requests, json
logger = logging.getLogger(__name__)

# The CMS_API endpoint of the current Django App for published Janis to use
if settings.DEPLOYMENT_MODE != "LOCAL":
    CMS_API = f"https://{os.getenv('APPLICATION_NAME','')}.herokuapp.com/api/graphql"
else:
    CMS_API = None

def netlify_publish():
    logger.debug("netlify_publish() Starting task")
    CI_COA_PUBLISHER_URL = os.getenv("CI_COA_PUBLISHER_URL")
    try:
        publish_janis_branch = getattr(JanisBranchSettings.objects.first(), 'publish_janis_branch')
    except:
        publish_janis_branch = None

    if publish_janis_branch and CMS_API:
        requests.post(
            url=f"CI_COA_PUBLISHER_URL/publish",
            data=json.dumps({
                "janis_branch": publish_janis_branch,
                "CMS_API": CMS_API,
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

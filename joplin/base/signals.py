from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from wagtail.core.signals import page_published, page_unpublished

import heroku3
from heroku3.models.build import Build

from base.models import TranslatedImage

import logging
logger = logging.getLogger(__name__)

IMAGE_WIDTHS = (
    640,  # iPhone 5/SE
    720,  # 720p non retina displays
    750,  # iPhone 6/7/8/X
    828,  # iPhone 6/7/8 Plus
    1080,  # 1080p non retina displays
    1440,  # 1440p non retina displays/720 retina displays
    2160,  # 1080p retina displays
)
JANIS_SLUG_URL = settings.JANIS_SLUG_URL


@receiver(post_save, sender=TranslatedImage)
def generate_responsive_images(sender, **kwargs):
    image = kwargs['instance']
    for width in IMAGE_WIDTHS:
        logger.debug(f'Generating image rendition for {width}px')
        image.get_rendition(f'width-{width}')


def create_build_if_configured():
    if not all([settings.HEROKU_KEY, settings.HEROKU_JANIS_APP_NAME]):
        logger.warning('Not triggering Janis build because the required settings are not configured.')
        logger.warning(f'HEROKU_KEY={settings.HEROKU_KEY}')
        logger.warning(f'HEROKU_JANIS_APP_NAME={settings.HEROKU_JANIS_APP_NAME}')
        return

    heroku = heroku3.from_key(settings.HEROKU_KEY)
    app = heroku.apps()[settings.HEROKU_JANIS_APP_NAME]

    build = create_build(heroku, app, JANIS_SLUG_URL)
    logger.info(f'Created build {build}')


def create_build(heroku, app, url, checksum=None, version=None, buildpack_urls=None):
    """Create a new release for this app.
       NOTE: Adapted from heroku3.py's create_release
       https://github.com/martyzz1/heroku3.py/blob/8b691c123e039204ad460ae6cf91e98de96a597e/heroku3/models/app.py#L507-L517
    """
    buildpack_urls = buildpack_urls or []
    payload = {
        'source_blob': {
            'url': url,
            'checksum': checksum,
            'version': version,
        },
        'buildpacks': [{'url': buildpack_url} for buildpack_url in buildpack_urls],
    }

    resp = heroku._http_resource(
        method='POST',
        resource=('apps', app.name, 'builds'),
        data=heroku._resource_serialize(payload),
    )
    resp.raise_for_status()

    item = heroku._resource_deserialize(resp.text)
    return Build.new_from_dict(item, h=heroku, app=app)


@receiver(page_published)
def page_published_signal(sender, **kwargs):
    logger.debug(f'page_published {sender}')
    create_build_if_configured()


@receiver(page_unpublished)
def page_unpublished_signal(sender, **kwargs):
    logger.debug(f'page_unpublished {sender}')
    create_build_if_configured()

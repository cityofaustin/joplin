from django.dispatch import receiver
from django.db.models.signals import post_save
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


@receiver(post_save, sender=TranslatedImage)
def generate_responsive_images(sender, **kwargs):
    image = kwargs['instance']
    for width in IMAGE_WIDTHS:
        logger.debug(f'Generating image rendition for {width}px')
        image.get_rendition(f'width-{width}')

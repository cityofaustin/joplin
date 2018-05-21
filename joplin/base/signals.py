from django.dispatch import receiver
from django.db.models.signals import post_save
from base.models import TranslatedImage

@receiver(post_save, sender=TranslatedImage)
def generate_responsive_images(sender, **kwargs):
    image = kwargs['instance']
    image.get_rendition('original')
    image.get_rendition('width-320') #iPhone 5/SE
    image.get_rendition('width-375') #iPhone 6/7/8/X
    image.get_rendition('width-414') #iPhone 6/7/8 Plus
    # TODO: get_rendition for other widths we want
    # TODO: retina resultions

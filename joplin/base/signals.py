from django.dispatch import receiver
from django.db.models.signals import post_save
from base.models import TranslatedImage

@receiver(post_save, sender=TranslatedImage)
def generate_responsive_images(sender, **kwargs):
    image = kwargs['instance']
    image.get_rendition('width-640') #iPhone 5/SE
    image.get_rendition('width-720') #720p non retina displays
    image.get_rendition('width-750') #iPhone 6/7/8/X
    image.get_rendition('width-828') #iPhone 6/7/8 Plus
    image.get_rendition('width-1080') #1080p non retina displays
    image.get_rendition('width-1440') #1440p non retina displays/720 retina displays
    image.get_rendition('width-2160') #1080p retina displays

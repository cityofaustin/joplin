from django.dispatch import receiver
from django.db.models.signals import post_save
from base.models import TranslatedImage
from django.urls import reverse
from wagtail.images.views.serve import generate_signature

@receiver(post_save, sender=TranslatedImage)
def generate_responsive_urls(sender, **kwargs):
    print("SAVE HAPPENED!")
    print(sender)
    image = kwargs['instance']
    generate_image_url(image, 'fill-100x100')

def generate_image_url(image, filter_spec):
    signature = generate_signature(image.id, filter_spec)
    url = reverse('wagtailimages_serve', args=(signature, image.id, filter_spec))

    # Append image's original filename to the URL (optional)
    url += image.file.name[len('original_images/'):]

    return url

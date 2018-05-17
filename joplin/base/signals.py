from django.dispatch import receiver
from django.db.models.signals import post_save
from base.models import TranslatedImage

@receiver(post_save, sender=TranslatedImage)
def post_save_callback(sender, **kwargs):
    print("SAVE HAPPENED!")
    print(sender)

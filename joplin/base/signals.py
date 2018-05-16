import django.dispatch

blarg = django.dispatch.Signal()

from django.dispatch import receiver

@receiver(blarg)
def my_callback(sender, **kwargs):
    print("Request finished!")

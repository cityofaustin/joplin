import django.dispatch
from django.dispatch import receiver

blarg = django.dispatch.Signal()

@receiver(blarg)
def blarg_callback(sender, **kwargs):
    print("BLARG HAPPENED!")

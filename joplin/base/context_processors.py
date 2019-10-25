from django.conf import settings


def settings_context(request):
    return {
    'JANIS_URL': settings.JANIS_URL,
    'ISPRODUCTION': settings.ISPRODUCTION
    }

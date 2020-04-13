from django.conf import settings


def settings_context(request):
    """
    Django's preferred way of sending enviornment/build variables
    into the app for templates and other contexual stuff
    """
    return {
        'JANIS_URL': settings.JANIS_URL,
        'IS_PRODUCTION': settings.IS_PRODUCTION
    }

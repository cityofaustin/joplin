from django.contrib.auth.models import Group


def translators():
    '''
    Members of the "Translators" group will receive an automated report every Monday and Wednesday
    about which pages have been published and need to be translated.
    This report is run by the command send_translation_report
    '''
    try:
        translators_group = Group.objects.get(name="Translators")
    except Group.DoesNotExist:
        translators_group = Group.objects.create(name="Translators")
    return translators_group

from groups.models import AdditionalGroup


def translators():
    '''
    Members of the "Translators" group will receive an automated report every Monday and Wednesday
    about which pages have been published and need to be translated.
    This report is run by the command send_translation_report
    '''
    try:
        translators_group = AdditionalGroup.objects.get(name="Translators")
    except AdditionalGroup.DoesNotExist:
        translators_group = AdditionalGroup.objects.create(name="Translators")
    return translators_group

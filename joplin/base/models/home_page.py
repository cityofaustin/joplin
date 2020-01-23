from django.db import models

from wagtail.core.models import Page

from .translated_image import TranslatedImage


class HomePage(Page):
    parent_page_types = []
    # subpage_types = ['base.ServicePage', 'base.ProcessPage', 'base.InformationPage', 'base.DepartmentPage']
    subpage_types = [
        'base.ServicePage',
        'base.ProcessPage',
        'informations.InformationPage',
        'base.DepartmentPage',
        'base.TopicPage',
        'locations.LocationPage'
    ]

    image = models.ForeignKey(TranslatedImage, null=True, on_delete=models.SET_NULL, related_name='+')

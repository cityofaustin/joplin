from django.db import models

from wagtail.core.models import Page

from .translated_image import TranslatedImage


class HomePage(Page):
    """
    right now this just controls which pages can be added to root,
    eventually we'd like to expand this to cover components that comprise the
    home page in janis, such as header, footer stuff and top services
    """
    parent_page_types = []
    # subpage_types = ['base.ServicePage', 'base.ProcessPage', 'base.InformationPage', 'base.DepartmentPage']
    subpage_types = ['base.ServicePage', 'base.ProcessPage', 'base.InformationPage', 'base.DepartmentPage', 'base.TopicPage']

    image = models.ForeignKey(TranslatedImage, null=True, on_delete=models.SET_NULL, related_name='+')

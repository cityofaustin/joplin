from django.db import models

from wagtail.core.models import Page

class HomePage(Page):
    parent_page_types = []
    # subpage_types = ['base.ServicePage', 'base.ProcessPage', 'base.InformationPage', 'base.DepartmentPage']
    subpage_types = [
        'service_page.ServicePage',
        'information_page.InformationPage',
        'department_page.DepartmentPage',
        'topic_page.TopicPage',
        'location_page.LocationPage',
        'event_page.EventPage'
    ]

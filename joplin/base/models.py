from django.db import models

from modelcluster.models import ClusterableModel

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsnippets.models import register_snippet


from wagtail.api import APIField


class HomePage(Page):
    pass


@register_snippet
class Event(ClusterableModel):
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    address = models.CharField(max_length=255)
    event_fees = models.CharField(max_length=255)


@register_snippet
class Department(ClusterableModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    hours = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.CharField(max_length=255)
    director_name = models.CharField(max_length=255)

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('address'),
        FieldPanel('hours'),
        FieldPanel('phone_number'),
        FieldPanel('email'),
        FieldPanel('description'),
        FieldPanel('director_name'),
    ]

    api_fields = [
        APIField('name'),
        APIField('address'),
        APIField('email'),
    ]

from django.db import models

from wagtail.snippets.models import register_snippet
from modelcluster.models import ClusterableModel
from wagtail.core.fields import StreamField
from wagtail.core.blocks import URLBlock
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from .location import Location

from .constants import DEFAULT_MAX_LENGTH

@register_snippet
class Contact(ClusterableModel):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    email = models.EmailField()
    phone = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    location = models.ForeignKey(Location, null=True, blank=True, related_name='+', on_delete=models.SET_NULL)

    social_media = StreamField(
        [
            ('url', URLBlock(
                label='Social media url'
            ))
        ],
        verbose_name='Links to any social media pages',
        help_text='For example: https://www.facebook.com/atxpoliceoversight/',
        blank=True
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('email'),
        FieldPanel('phone'),
        SnippetChooserPanel('location'),
        InlinePanel('hours', label='Hours'),
        StreamFieldPanel('social_media'),
    ]

    def __str__(self):
        return self.name

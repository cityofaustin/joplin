from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.models import Image
from wagtail.images.edit_handlers import ImageChooserPanel
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from base.models import JanisBasePage, HomePage
from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
    FieldRowPanel,
    StreamFieldPanel,
)
from base.models.translated_image import TranslatedImage
from base.models import Location as BaseLocation

# The abstract model for related links, complete with panels
from wagtail.core.fields import RichTextField, StreamField
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, HelpPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from base.models import JanisBasePage
from base.models.widgets import countMe, countMeTextArea, AUTHOR_LIMITS
from modelcluster.models import ClusterableModel
from base.models.constants import DEFAULT_MAX_LENGTH
from base.models.day_and_duration import DayAndDuration
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from wagtail.core import blocks


# from ls.joyous.models import EventBase


class EventPage(JanisBasePage):
    janis_url_page_type = 'event'

    # content_panels = [
    #     FieldPanel('title_en', widget=countMe),
    #     FieldPanel('title_es', widget=countMe),
    #     FieldPanel('title_ar'),
    #     FieldPanel('title_vi'),
    # ]
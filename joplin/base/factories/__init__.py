import factory
import wagtail_factories
from django.utils.text import slugify
from wagtail.core.models import Collection, Page
from wagtail.core.blocks import RichTextBlock, TextBlock
from base.models import *


class RichTextBlockFactory(wagtail_factories.StructBlockFactory):
    text = factory.LazyAttribute(lambda x: RichText('<h2>{}</h2>{}'.format(fake_title(), fake.text(max_nb_chars=300))))

    class Meta:
        model = RichTextBlock


class TextBlockFactory(wagtail_factories.blocks.BlockFactory):
    class Meta:
        model = TextBlock

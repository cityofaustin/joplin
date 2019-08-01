from django.db import models

from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import RichTextBlock
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel

from base.forms import InformationPageForm

from .janis_page import JanisPage

from .constants import WYSIWYG_GENERAL

class InformationPage(JanisPage):
    janis_url_page_type = "information"

    description = models.TextField(blank=True, verbose_name='Write a description of this page')
    options = StreamField(
        [
            ('option', RichTextBlock(
                features=WYSIWYG_GENERAL,
                label='Option'
            ))
        ],
        verbose_name='Add option sections as needed.',
        help_text='Options are needed when the reader needs to make a choice between a few options, such as ways to fill out a form (online, by phone, in person, etc.).',
        blank=True
    )

    additional_content = RichTextField(
        features=WYSIWYG_GENERAL,
        verbose_name='Write any additional content describing the service',
        blank=True
    )

    # TODO: Add images array field

    base_form_class = InformationPageForm

    content_panels = [
        FieldPanel('title_en'),
        FieldPanel('title_es'),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        InlinePanel('topics', label='Topics'),
        InlinePanel('related_departments', label='Related Departments'),
        FieldPanel('description'),
        StreamFieldPanel('options'),
        FieldPanel('additional_content'),
        InlinePanel('contacts', label='Contacts'),
    ]

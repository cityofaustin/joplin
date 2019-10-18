from django.db import models

from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from base.forms import FormPageForm

from .janis_page import JanisBasePage

from .constants import WYSIWYG_GENERAL
from .widgets import countMe, countMeTextArea
from countable_field import widgets

class FormPage(JanisBasePage):
    janis_url_page_type = "form"
    base_form_class = FormPageForm

    description = models.TextField(verbose_name='Write a description of this page', blank=True)
    script_tag = models.TextField(verbose_name='Enter the script tag from Formstack', blank=True)

    content_panels = [
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('description', widget=countMeTextArea),
        FieldPanel('script_tag'),
    ]

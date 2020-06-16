from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel

from base.forms import FormContainerForm

from base.models.widgets import countMe, countMeTextArea
from publish_preflight.requirements import FieldPublishRequirement, RelationPublishRequirement, ConditionalPublishRequirement, DepartmentPublishRequirement

from pages.topic_page.models import JanisBasePageWithTopics


class FormContainer(JanisBasePageWithTopics):
    janis_url_page_type = "form"
    base_form_class = FormContainerForm

    description = models.TextField(verbose_name='Form description', blank=True)
    form_url = models.URLField(
        verbose_name='Enter the URL of your Formstack form',
        help_text='This link can be found under Share > "Link to this form on your website or email:"',
        blank=True,
    )

    publish_requirements = (
        FieldPublishRequirement("description", langs=["en"]),
        FieldPublishRequirement("form_url", langs=["en"]),
        ConditionalPublishRequirement(
            RelationPublishRequirement("topics"),
            "or",
            DepartmentPublishRequirement(),
            message="You must have at least 1 topic or 1 department selected.",
        ),
    )

    content_panels = [
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        InlinePanel('topics', label='Topics'),
        FieldPanel('description', widget=countMeTextArea),
        FieldPanel('form_url'),
    ]

from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel

from base.forms import FormContainerForm

from .janis_page import JanisBasePage

from .widgets import countMe, countMeTextArea
from publish_preflight.requirements import FieldPublishRequirement, RelationPublishRequirement, ConditionalPublishRequirement

class FormContainer(JanisBasePage):
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
            RelationPublishRequirement("related_departments"),
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

class FormContainerTopic(ClusterableModel):
    page = ParentalKey(FormContainer, related_name='topics')
    topic = models.ForeignKey('base.TopicPage', verbose_name='Select a Topic', related_name='+', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('topic'),
    ]

    def __str__(self):
        return self.topic.text

from django.db import models
# from wagtail_modeltranslation.translation import register, TranslationOptions

from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from base.forms import ServicePageForm

from pages.base_page.models import JanisBasePage
from pages.department_page.models import DepartmentPage
from snippets.contact.models import Contact

from base.models.widgets import countMe

from publish_preflight.requirements import FieldPublishRequirement, RelationPublishRequirement

from publish_preflight.forms import PublishPreflightForm

WYSIWYG_MEDIA_RELEASE_BODY = ['ul', 'ol', 'link']


class MediaReleasePageForm(PublishPreflightForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MediaReleasePage(JanisBasePage):
    janis_url_page_type = "blargy"

    body = RichTextField(
        features=WYSIWYG_MEDIA_RELEASE_BODY,
        verbose_name='Body',
        blank=True
    )

    base_form_class = ServicePageForm

    contact = models.ForeignKey(Contact, blank=True, null=True, on_delete=models.SET_NULL)

    written_for_department = models.ForeignKey(DepartmentPage, blank=True, null=True, on_delete=models.SET_NULL)

    publish_requirements = (
        FieldPublishRequirement("body", message="🤠 can't publish without a body 🌵", langs=["en"]),
        RelationPublishRequirement("contact", message="🤠 can't publish without a contact 🌵"),
    )

    content_panels = [
        # todo: we want these to say headline, not title
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('body'),
        SnippetChooserPanel('contact'),
        PageChooserPanel('written_for_department', page_type=DepartmentPage)
    ]


# @register(MediaReleasePage)
# class MediaReleasePageTranslationOptions(TranslationOptions):
#     fields = (
#         'body',
#     )

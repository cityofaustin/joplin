from django.db import models

from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from base.forms import ServicePageForm

from pages.base_page.models import JanisBasePage
from pages.department_page.models import DepartmentPage
from snippets.contact.models import Contact

from base.models.widgets import countMe

from publish_preflight.requirements import FieldPublishRequirement, DepartmentPublishRequirement

from publish_preflight.forms import PublishPreflightForm

WYSIWYG_NEWS_BODY = ['ul', 'ol', 'link']


class NewsPageForm(PublishPreflightForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NewsPage(JanisBasePage):
    janis_url_page_type = "news"

    body = RichTextField(
        features=WYSIWYG_NEWS_BODY,
        verbose_name='Body',
        blank=True
    )

    base_form_class = ServicePageForm

    contact = models.ForeignKey(Contact, blank=True, null=True, on_delete=models.SET_NULL)

    written_for_department = models.ForeignKey(DepartmentPage, blank=True, null=True, on_delete=models.SET_NULL,
                                               verbose_name="Assign a different department",
                                               help_text="If this news is written for another department, select that department below. This ensures that this news is associated with that department's news content")

    publish_requirements = (
        FieldPublishRequirement("body", message="Body text is required to publish", langs=["en"]),
        FieldPublishRequirement("contact", message="A contact is required to publish"),
        DepartmentPublishRequirement(message="🤠 can't publish without a department, this should only happen to admins that forgot to pick a department in the modal, or users that aren't in a department group. This requirement will not be satisfied by the 'different department' field 🌵"),
    )

    content_panels = [
        # todo: we want these to say headline, not title
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('body'),
        PageChooserPanel('written_for_department', page_type=DepartmentPage),
        SnippetChooserPanel('contact')
    ]

    def janis_urls(self):
        return [instance['url'] for instance in self.janis_instances()]

    def janis_instances(self):
        # If we have a different department, publish under that department only
        if self.written_for_department and self.written_for_department != self.departments()[0]:
            by_department = self.departments()[0]

            return [
                {'url': f'/{self.written_for_department.slug_en}/{self.slug_en}/',
                 'parent': self.written_for_department, 'grandparent': None,
                 'from_department': self.written_for_department,
                 'by_department': by_department}]

        # If we don't have a written_for department, publish under the default departments
        return [{'url': f'/{department.slug_en}/{self.slug_en}/',
                 'parent': department,
                 'grandparent': None,
                 'from_department': department,
                 'by_department': None}
                for department in self.departments()]

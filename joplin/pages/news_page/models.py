from django.db import models

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

WYSIWYG_NEWS_BODY = ['ul', 'ol', 'link']


class MediaReleasePageForm(PublishPreflightForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NewsPage(JanisBasePage):
    janis_url_page_type = "blargy"

    body = RichTextField(
        features=WYSIWYG_NEWS_BODY,
        verbose_name='Body',
        blank=True
    )

    base_form_class = ServicePageForm

    contact = models.ForeignKey(Contact, blank=True, null=True, on_delete=models.SET_NULL)

    written_for_department = models.ForeignKey(DepartmentPage, blank=True, null=True, on_delete=models.SET_NULL)

    publish_requirements = (
        FieldPublishRequirement("body", message="🤠 can't publish without a body 🌵", langs=["en"]),
        FieldPublishRequirement("contact", message="🤠 can't publish without a contact 🌵"),
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

    def janis_urls(self):
        return [instance['url'] for instance in self.janis_instances()]

    def janis_instances(self):
        """
        News pages have logic around the written_for_department field
        if it is filled in, we want to publish there instead of under out normal department
        """

        # If we have a "different" department, publish under that department only
        if self.written_for_department:
            by_department = self.departments()[0]
            blarg = 0

            return [
                {'url': f'/{self.written_for_department}/{self.slug_en}/',
                 'parent': self.written_for_department, 'grandparent': None,
                 'from': self.written_for_department,
                 'by': by_department}]

        bllll = self.departments()
        # If we don't have a "different" department, publish under the default departments
        return [{'url': f'/{department.slug_en}/{self.slug_en}/',
                 'parent': department,
                 'grandparent': None,
                 'from': department,
                 'by': None}
                for department in self.departments()]

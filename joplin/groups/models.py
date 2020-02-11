from django.contrib.auth.models import Group
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from modelcluster.models import ClusterableModel
from wagtail.snippets.models import register_snippet


@register_snippet
class Department(ClusterableModel, Group):
    department_page = models.OneToOneField(
        "base.departmentPage",
        on_delete=models.CASCADE,
        primary_key=True,
    )

    panels = [
        FieldPanel('name'),
        PageChooserPanel("department_page"),
    ]

    def __str__(self):
        return self.name





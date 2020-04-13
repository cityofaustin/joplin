from django.contrib.auth.models import Group
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from modelcluster.models import ClusterableModel


class Department(ClusterableModel, Group):
    department_page = models.OneToOneField(
        "base.departmentPage",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    panels = [
        FieldPanel('name'),
        PageChooserPanel("department_page"),
    ]

    class Meta:
        verbose_name_plural = "Departments"
        ordering = ['name']

    def __str__(self):
        return self.name

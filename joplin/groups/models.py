from django.contrib.auth.models import Group
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from modelcluster.models import ClusterableModel


class Department(ClusterableModel, Group):
    department_page = models.OneToOneField(
        "department_page.departmentPage",
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


class AdditionalGroup(ClusterableModel, Group):
    '''
        So far, "Translators" is the only other "AdditionalGroup" that we have.
        A member of "Translators" will receive an automated report every Monday and Wednesday
        about which pages have been published and need to be translated.
    '''
    panels = [
        FieldPanel('name'),
    ]

    class Meta:
        verbose_name_plural = "NonEditorGroups"
        ordering = ['name']

    def __str__(self):
        return self.name

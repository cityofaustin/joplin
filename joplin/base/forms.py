from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.core.models import Page, PageRevision
from django.core.exceptions import ValidationError
from wagtail.admin import messages


class JanisPageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        ways to limit scope:
        changed fields,
        then exclude fields that are required

        self.changed_data = list of fields changed

        self[field_name].data or as_text (might be useful for streamfields)
        looks like this is working, atm tho it just wont let you publish any empty fields :-D
        """
        def check_for_empties(form_entries):
            entries = []
            # alt structure to explore: self.fields[entry]
            for entry in form_entries:
                # TODO really only works for strings atm, super lazy hack to ignore streamfields and prevent render error
                if not self[entry].data and str(type(self.fields[entry])) == "<class 'django.forms.fields.CharField'>":
                    self.add_error(entry, ValidationError((f'{entry} is empty!'), code='invalid'))
                    entries.append(entry)
            return entries

        def check_for_missing_relations():
            relations = self.formsets
            {
                relation_name: self.add_error(None, f'No {relation_name} selected')
                for (relation_name, value) in relations.items()
                if not value.forms
            }

        cleaned_data = super().clean()

        if 'action-publish' in self.data:
            # TODO: we'll probably want a good way to check a managed subset
            all_keys = list(self.fields.keys())
            check_all = check_for_empties(all_keys)
            missing_relations = check_for_missing_relations()
        return cleaned_data


class ServicePageForm(JanisPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProcessPageForm(JanisPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InformationPageForm(JanisPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DepartmentPageForm(JanisPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TopicPageForm(JanisPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TopicCollectionPageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OfficialDocumentPageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GuidePageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class FormPageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

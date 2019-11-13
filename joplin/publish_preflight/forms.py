from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.core.models import Page, PageRevision
from django.core.exceptions import ValidationError
from wagtail.admin import messages


class PublishPreflightForm(WagtailAdminPageForm):
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
        def check_for_empties():
            errors_for_empties = {
                field_name: try_adding_error_to_field(field_name, field_value)
                for (field_name, field_value) in self.data.items()
                if len(field_value) == 0
            }

        def try_adding_error_to_field(field_name, field_value):
            try:
                self.add_error(field_name, f'{field_name} is empty!')
            except ValueError as e:
                print(e)
                try:
                    field_value.non_form_errors().append(f'{field_name} not selected!')
                    self.add_error(None, f'{field_name} is missing!')
                except AttributeError as e:
                    print(e)
                    pass
                pass

        def check_for_missing_relations():
            relations = self.formsets
            # relation_value.cleaned_data
            errors_for_missing_relations = {
                relation_name: try_adding_error_to_field(relation_name, relation_value)
                for (relation_name, relation_value) in relations.items()
                if not relation_value.forms
            }

        cleaned_data = super().clean()

        if 'action-publish' in self.data:
            # TODO: we'll probably want a good way to check a managed subset
            all_keys = list(self.fields.keys())
            check_all = check_for_empties()
            missing_relations = check_for_missing_relations()

        return cleaned_data

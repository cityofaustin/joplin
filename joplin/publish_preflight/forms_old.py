from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.core.models import Page, PageRevision
from django.core.exceptions import ValidationError
from wagtail.admin import messages
import logging


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

        # self.data.items()
        def check_for_empties():
            """
            adds an error to each field if it is empty
            """
            if hasattr(self.instance, 'fields_required_for_publish'):
                errors_for_empties = {
                    field_name: try_adding_error_to_field(
                        field_name, field_value)
                    for (field_name, field_value) in self.data.items()
                    if (len(field_value) == 0 or field_value == 'null') and field_name in self.instance.fields_required_for_publish
                }

        def try_adding_error_to_field(field_name, field_value):
            try:
                self.add_error(field_name, f'{field_name} is empty!')
            except ValueError as e:
                logging.error(e)
                try:
                    field_value.non_form_errors().append(
                        f'{field_name} not selected!')
                    self.add_error(None, f'{field_name} is missing!')
                except AttributeError as e:
                    logging.error(e)
                    pass
                pass

        # self.formsets
        # self if its an empty array realtion.forms != []
        def check_for_missing_relations():
            relations = self.formsets
            # relation_value.cleaned_data
            if hasattr(self.instance, 'fields_required_for_publish'):
                errors_for_missing_relations = {
                    relation_name: try_adding_error_to_field(
                        relation_name, relation_value)
                    for (relation_name, relation_value) in relations.items()
                    if not relation_value.forms and relation_name in self.instance.fields_required_for_publish
                }

        cleaned_data = super().clean()

        if 'action-publish' in self.data:
            # TODO: we'll probably want a good way to check a managed subset
            print("Publish!")
            all_keys = list(self.fields.keys())
            check_all = check_for_empties()
            missing_relations = check_for_missing_relations()

        return cleaned_data

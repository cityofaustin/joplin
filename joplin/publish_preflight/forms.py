from wagtail.admin.forms import WagtailAdminPageForm

# Some types of errors (such as ValidationError) don't get propagated by Django within the clean() function.
# So we create a wrapper PublishException class that will throw errors when appropriate
class PublishException(BaseException):
    pass


class PublishPreflightForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_error_to_edit_page(self, field_name, message):
        try:
            """
                This method allows adding errors to specific fields from within the Form.clean() method, 
                or from outside the form altogether; for instance from a view.
            """
            # if the section wasn't added to the consolidated data, there isnt a place for the message to attach to
            self.add_error(field_name, message)
        except ValueError as e:
            raise PublishException("An error occurred while handling unmet Publishing criteria") from e

    '''
    This method can also be called directly on page.json().
    This is useful for our custom /publish endpoint that doesn't have a Form instance created from an edit page request.
    page.base_form_class.check_publish_requirements(
        page.publish_requirements,
        page.to_json()
    )
    Returns a list of unmet criteria. If the form passes successfully, the return value will be an empty list.
    '''
    @staticmethod
    def check_publish_requirements(publish_requirements, data):
        try:
            unmet_criteria = []
            for requirement in publish_requirements:
                result = requirement.check_criteria(data)
                if not result["result"]:
                    unmet_criteria.append(result)
            print('unmet criteria, l42', unmet_criteria)
            return unmet_criteria
        except BaseException as e:
            raise PublishException("An error occurred during publishing") from e

    # Overrides default clean() method
    # This is executed by form.is_valid() in the edit() handler in wagtail/admin/views/pages.py
    def clean(self):
        cleaned_data = super().clean()

        # Check publish requirements, add errors if any are unmet
        if self.data['action-publish'] == 'action-publish':
            if hasattr(self.instance, "publish_requirements"):
                consolidated_data = cleaned_data
                # TODO add formset data to consolidated_data
                publish_requirements = self.instance.publish_requirements
                # collect the requirements that arent filled out
                unmet_criteria = self.check_publish_requirements(publish_requirements, consolidated_data)
                for result in unmet_criteria:
                    self.add_error_to_edit_page(result["field_name"], result["message"])
        return cleaned_data

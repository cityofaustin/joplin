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
            self.add_error(field_name, message)
        except ValueError as e:
            raise PublishException("An error occured while handling unmet Publishing criteria") from e

    # Overrides default clean() method
    # This is executed by form.is_valid() in the edit() handler in wagtail/admin/views/pages.py
    def clean(self):
        cleaned_data = super().clean()

        # Check publish requirements, add errors if any are unmet
        if (self.data['action-publish'] == 'action-publish'):
            if hasattr(self.instance, "publish_requirements"):
                publish_requirements = self.instance.publish_requirements
                try:
                    unmet_criteria = []
                    for requirement in publish_requirements:
                        result = requirement.check_criteria(self)
                        if not result["result"]:
                            unmet_criteria.append(result)
                    for result in unmet_criteria:
                        self.add_error_to_edit_page(result["field_name"], result["message"])
                except BaseException as e:
                    raise PublishException("An error occured during publishing") from e
        return cleaned_data

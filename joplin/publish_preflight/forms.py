from wagtail.admin.forms import WagtailAdminPageForm

class PublishPreflightForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Overrides default clean() method
    # This is executed by form.is_valid() in the edit() handler in wagtail/admin/views/pages.py
    def clean(self):
        cleaned_data = super().clean()

        # Check publish requirements, add errors if any are unmet
        if (self.data['action-publish'] == 'action-publish'):
            if hasattr(self.instance, "publish_requirements"):
                publish_requirements = self.instance.publish_requirements
                unmet_criteria = []
                for requirement in publish_requirements:
                    result = requirement.check_criteria(self)
                    if not result["passed"]:
                        self.add_error(None, result["publish_requirement_error"])

        return cleaned_data

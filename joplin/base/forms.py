from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.core.models import Page, PageRevision
from django.core.exceptions import ValidationError

# copying Sergio's magic code


def get_http_request():
    """
        Probably a bad-practice & non-performant approach,
        returns a django request object.
        https://docs.djangoproject.com/en/2.2/ref/request-response/
    """
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            # looking good...
            return frame_record[0].f_locals['request']
            break
    else:
        # looking bad...
        return None


class ServicePageForm(WagtailAdminPageForm):
    def clean(self):
        """
        ways to limit scope:
        changed fields,
        then exclude fields that are required

        self.changed_data = list of fields changed

        self[field_name].data or as_text (might be useful for streamfields)
        looks like this is working, atm tho it just wont let you publish any empty fields :-D
        """

        # TODO figure out a way to check if its publish vs draft, maybe compare page revisions?
        cleaned_data = super().clean()
        request = get_http_request()
        is_publishing = bool(request.POST.get('action-publish'))
        if is_publishing:
            field_keys = self.changed_data
            for field_key in field_keys:
                if not self[field_key].data:
                    self.add_error(field_key, "It's empty!")
                    ValidationError(('Invalid value, empty'), code='invalid')
        return cleaned_data


class ProcessPageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InformationPageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DepartmentPageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TopicPageForm(WagtailAdminPageForm):
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

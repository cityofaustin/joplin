from wagtail.wagtailadmin.forms import WagtailAdminPageForm


class ServicePageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

from wagtail.wagtailadmin.forms import WagtailAdminPageForm


class ServicePageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: There should be a more elegant way to do this
        self.fields['content_es'].help_text = self.instance.content
        self.fields['content_vi'].help_text = self.instance.content
        self.fields['content_zh_hans'].help_text = self.instance.content
        self.fields['content_zh_hant'].help_text = self.instance.content

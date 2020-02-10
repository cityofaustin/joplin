from django import template

register = template.Library()

@register.filter(name='extract_publish_error_data')
def extract_publish_error_data(form):
    if hasattr(form, "_errors") and form._errors:
        form_errors = form._errors.get("__all__", None)
        if form_errors:
            return [i.publish_error_data for i in form_errors.data if hasattr(i, "publish_error_data")]
    return []
